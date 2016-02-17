import httplib
import json
import sys
import base64

# head = {"Content-Type": "application/json", "Accept": "application/json"}

def get(conn):
	"""Get the response following a rpc() (http GET or POST) call."""
	try:
		r1 = conn.getresponse()
	except Exception as e:
		return (None, e)
	if r1.status < 200 or r1.status > 299:
		_ = r1.read()
		return (None, "%s %s (%s)" % (r1.status, r1.reason, _))
	d1 = r1.read()
	try:
		j = json.loads(d1)
	except:
		j = None
	return (j, "%s %s" % (r1.status, r1.reason))

def http_delete(conn, id):
	uri = "/%s?from=http://localhost:10000&requestIdentifier=12345" % (id)
	head = {"Content-Type": "application/json", "Accept": "application/json"}
	try:
		conn.request("DELETE", uri, "", head)
	except Exception as e:
		return (None, e)
	return get(conn)

def http_retrieve(conn, id):
	uri = "/%s?from=http://localhost:10000&requestIdentifier=12345" % (id)
	head = {"Content-Type": "application/json", "Accept": "application/json"}
	try:
		conn.request("GET", uri, "", head)
	except Exception as e:
		return (None, e)
	return get(conn)

def http_create(conn, parent, restype, attr):
	a = ""
	if attr != None:
		n = len(attr)
		sep = ","
		c = 1
		for i in attr:
			if n == c:
				sep = ""
			a = a + '"%s": "%s"%s\n' % (i, attr[i], sep)
			c = c + 1
	uri = "/%s?from=http://localhost:10000&requestIdentifier=12345" % (parent)
	head = {"Content-Type": "application/json", "Accept": "application/json"}
	body = '''
		{
			"from": "http://localhost:10000",
			"requestIdentifier": "12345",
			"resourceType": "%s",
			"content": {
				%s
			}
		}
	''' % (restype, a)
	#print "uri", uri
	#print "body", body
	#print "head", head
	try:
		conn.request("POST", uri, body, head)
	except Exception as e:
		return (None, e)
	return get(conn)

def http_update(conn, id, attr):
	a = ""
	if attr != None:
		n = len(attr)
		sep = ","
		c = 1
		for i in attr:
			if n == c:
				sep = ""
			a = a + '"%s": "%s"%s\n' % (i, attr[i], sep)
			c = c + 1
	uri = "/%s?from=http://localhost:10000&requestIdentifier=12345" % (id)
	head = {"Content-Type": "application/json", "Accept": "application/json"}
	body = '''
		{
			"from": "http://localhost:10000",
			"requestIdentifier": "12345",
			"content": {
				%s
			}
		}
	''' % (a)
	print "uri", uri
	print "head", head
	print "body", body
	try:
		conn.request("PUT", uri, body, head)
	except Exception as e:
		return (None, e)
	return get(conn)

def tree(conn, head):
	"""Ask DDM for a JSON version of the datastore"""
	fn = "/restconf/operational/oneM2M-cSEBase:cSEBase"
	try:
		conn.request("GET", fn, "", head)
	except Exception as e:
		return (None, e)
	(r, t) = get(conn)
	return (r,t)

def rpc(conn, head, fn, body):
	"""Ask DDM to perform a RPC call based on the function URI and JSON arguments"""
	if body == None:
		return (None, "empty body")
	try:
		s = "/restconf/operations/oneM2M-cSEBase:" + fn + "Resource"
		conn.request("POST", s, body, head)
	except Exception as e:
		return (None, e)
	(r, t) = get(conn)
	return (r, t)

def make_delete(id):
	"""Construct a JSON message to delete the given resource ID"""
	if id == None:
		return None
	return '{ "input": { "resourceURI": "' + id + '" } }'

def make_update(id, attr=None):
	"""Construct a JSON message to update the given resource ID with the attribute name/value pairs in the given dictionary"""
	if id == None:
		return None
	attrib = ""
	if type(attr) is dict:
		for i in attr:
			attrib = attrib + '{ "attributeName": "%s", "attributeValue": "%s" },' % (i, attr[i])
	return '{ "input": { "Attributes": [ %s ], "resourceURI": "%s" } }' % (attrib, id)

def make_retrieve(id, Disrestype=None, ResultContent=None):
	"""Construct a JSON message to retrieve the given resource ID with optional extra attributes"""
	# ResultContent
	# Disrestype
	if id == None:
		return None
	a = '{ "input": { "resourceURI": "%s"' % (id)
	if Disrestype != None:
		a = a + ', "Disrestype" : "%s"' % (Disrestype)
	if ResultContent != None:
		a = a + ', "ResultContent" : "%s"' % (ResultContent)
	a = a + " } }"
	return a

def make_create(id, restype, attr=None):
	"""Construct a JSON message to create a new resource as a child of the given resource ID with the optional attribute name/value pair dictionary"""
	if id == None:
		return None
	if restype == None:
		return None
	attrib = ""
	if type(attr) is dict:
		for i in attr:
			attrib = attrib + '{ "attributeName": "%s", "attributeValue": "%s" },' % (i, attr[i])
	return '''
	{
		"input": {
			"Attributes": [
				{ "attributeName": "resourceType", "attributeValue": "%s" },
				%s
			],
			"resourceURI": "%s"
		}
	}
	''' % (restype, attrib, id)

#!/usr/bin/python

import ddm
import sys

def _find(parentid, id, restype, x, token):
	if not 'Attributes' in x['output']['ResourceOutput'][0]:
		return
	attr = x['output']['ResourceOutput'][0]['Attributes']
	for i in attr:
		if 'attributeName' in i and i['attributeName'] == "labels" and 'attributeValue' in i:
			# see if we're using newiotdm or iotdm
			if i['attributeValue'].find("getLabelName") >= 0:
				fs = "getLabelName=" + token['what'] + ","
			else:
				fs = token['what']
			if i['attributeValue'] == fs:
				token['when'].append(parentid + "/" + id)


def internal_connect(server):
	"""Connect to the DDM server at the given server address"""
	try:
		conn = httplib.HTTPConnection(server)
	except Exception as e:
		return (None, e)
	#conn.set_debuglevel(1)
	return (conn, "")

def isTree(res):
	"""Check if the given JSON dictionary is the output from a tree request"""
	if res == None:
		return False
	if 'cSEBase' in res and 'cSEBaseChild' in res['cSEBase']:
		return True
	return False

def hasAE(res):
	"""Check if the given tree request output has AE resources"""
	if isTree(res) and 'oneM2M-resourceAE:resourceAE' in res['cSEBase']['cSEBaseChild']:
		return True
	return False

def getAE(res):
	"""Return the portion of a tree request output with AE resources"""
	if hasAE(res):
		return res['cSEBase']['cSEBaseChild']['oneM2M-resourceAE:resourceAE']

def hasContainer(res):
	"""Check if the given tree request output has container resources"""
	if isTree(res) and 'oneM2M-resourceContainer:resourceContainer' in res['cSEBase']['cSEBaseChild']:
		return True
	return False

def getContainer(res):
	"""Return the portion of a tree request output with container resources"""
	if hasContainer(res):
		return res['cSEBase']['cSEBaseChild']['oneM2M-resourceContainer:resourceContainer']

def isResult(d):
	"""Check if the given dictionary is the result of a CRUD request"""
	if not type(d) is dict:
		return False
	if not ('output' in d and 'content' in d['output']):
		return False
	return True
'''
{u'output':
	{
		u'content': u'Hierarchical path:InCSE1/10001/20001/30001',
		u'responseStatusCode': 2001,
		u'responseIdentifier': u'ResourceIdentifier',
		u'responseCode': u"STATUS_CREATED a 'contentInstance' "
	}
}
'''

def identifier(d):
	"""Return the response code of the given CRUD request"""
	if not isResult(d):
		return None
	return d['output']['responseIdentifier']

def code(d):
	"""Return the response code of the given CRUD request"""
	if not isResult(d):
		return None
	return d['output']['responseCode']

def status(d):
	"""Return the response code of the given CRUD request"""
	if not isResult(d):
		return None
	return d['output']['responseStatusCode']

def id(d):
	"""Return the resource ID of the given CRUD request"""
	if type(d) == type("string"):
		hp = "Hierarchical path:"
		s = d.find(hp)
		if s >= 0:
			e = d.find(",", s+len(hp))
			if e >= 0:
				return d[s+len(hp):e]
	if not isResult(d):
		return None
	a = d['output']['content'].split(",")
	if len(a) != 2:
		a = [d['output']['content']]
	b = a[0].split(":")
	if len(b) != 2:
		return None
	if b[1][0] == "/":
		return b[1][1:]
	return b[1]

def meta(r):
	"""Return DDM server information from a tree request"""
	if not isTree(r):
		return
	return r['cSEBase']['cSEBaseAttributes']

# This is the object constructor for a new connection to a DDM server

class connect:
	def __init__(self, server="localhost:8181", user="admin", pw="admin", proto="restconf"):
		"""Connect to a DDM server over-rideable defaults"""
		bu = base64.b64encode(user + ":" + pw).decode("ascii")
		self.head = {
			"Content-Type": "application/json",
			"Accept": "application/json",
			"Authorization" : "Basic %s" %
				base64.b64encode(user + ":" + pw).decode("ascii")
		}
		self.proto = proto
		self.server = server
		self.user = user
		self.pw = pw
		self.cachetree = None
		(self.conn, self.error) = internal_connect(server)
	def meta(self):
		"""Get and cache DDM server information if requested"""
		if self.cachetree == None:
			self.cachetree = self.tree()
		if isTree(self.cachetree):
			return meta(self.cachetree)
	def tree(self):
		"""Get and cache the resource tree"""
		(self.result,self.error) = tree(self.conn, self.head)
		if not self.result == None:
			self.cachetree = self.result
		return self.result
	def walk(self, fn, token=None, usecache=False):
		"""Walk through the resources in the provided tree calling the provided function with the provided arguments"""
		#r = self.cachetree
		#if usecache == False or self.cachetree == None:
		#	r = self.tree()
		r = self.tree()
		if not isTree(r):
			return
		if not hasAE(r):
			return
		for i in range(0, len(getAE(r))):
			me = getAE(r)[i]
			attr = me['resourceAEAttributes']
			x = self.retrieve(attr['parentID']+ "/" + attr['resourceName'])
			fn(attr['parentID'], attr['resourceName'], "AE", x, token)
		if not hasContainer(r):
			return
		for i in range(0, len(getContainer(r))):
			me = getContainer(r)[i]
			attr = me['resourceContainerAttributes']
			x = self.retrieve(attr['parentID']+ "/" + attr['resourceName'])
			fn(attr['parentID'], attr['resourceName'], "container", x, token)
			if 'resourceContainerChild' in me:
				if 'resourceContentInstance' in me['resourceContainerChild']:
					you = me['resourceContainerChild']['resourceContentInstance']
					for j in range(0, len(you)):
						attr = you[j]['resourceContentInstanceAttributes']
						x = self.retrieve(attr['parentID']+ "/" + attr['resourceName'])
						fn(attr['parentID'], attr['resourceName'], "contentInstance", x, token)
	def create(self, parent, restype, attr=None):
		"""Create a new resource as a child of the given resource ID with the optional attribute name/value pair dictionary"""
		if self.proto == "http":
			(self.result,self.error) = http_create(self.conn, parent, restype, attr)
		else:
			self.body = make_create(parent, restype, attr)
			(self.result,self.error) = rpc(self.conn, self.head, "create", self.body)
		return self.result
	def retrieve(self, id, Disrestype=None, ResultContent=None):
		"""Retrieve resource ID optionally with non-hierarchal output and/or child information"""
		if self.proto == "http":
			(self.result,self.error) = http_retrieve(self.conn, id)
		else:
			self.body = make_retrieve(id, Disrestype, ResultContent)
			(self.result,self.error) = rpc(self.conn, self.head, "retrieve", self.body)
		return self.result
	def update(self, id, attr=None):
		"""Update resource ID with attribute name/value pairs in the provided dictionary"""
		if self.proto == "http":
			(self.result,self.error) = http_update(self.conn, id, attr)
		else:
			self.body = make_update(id, attr)
			(self.result,self.error) = rpc(self.conn, self.head, "update", self.body)
		return self.result
	def delete(self, id):
		"""Delete the resource with the provided ID"""
		if self.proto == "http":
			(self.result,self.error) = http_delete(self.conn, id)
		else:
			self.body = make_delete(id)
			(self.result,self.error) = rpc(self.conn, self.head, "delete", self.body)
		return self.result
	def find(self, str, usecache=False):
		info = { "what": str, "when": [] }
		self.walk(_find, info, usecache)
		return info['when']

