"""This is the base library for criotdm. Both work for IoTDM project."""

import requests
from urlparse import urlparse
from OneM2M import http

op_provision = ":8181/restconf/operations/onem2m:onem2m-cse-provisioning"
op_tree = ":8181/restconf/operational/onem2m:onem2m-resource-tree"
op_cleanup = ":8181/restconf/operations/onem2m:onem2m-cleanup-store"

headers = http.default_headers
session = requests.Session()
timeout = 5

cse_payload = '''
{    "input": {
        "onem2m-primitive": [
           {
                "name": "CSE_ID",
                "value": "%s"
            },
            {
                "name": "CSE_TYPE",
                "value": "IN-CSE"
            }
        ]
    }
}
'''

# resourcepayload = '''
# {
#     %s
# }
# '''
#
# ae_payload = '''
# {
#     "m2m:ae":{%s}
# }
# '''
#
# cnt_payload = '''
# {
#     "m2m:cnt":{%s}
# }
# '''
#
# cin_payload = '''
# {
#    "m2m:cin":{%s}
# }
# '''
#
# sub_payload = '''
# {
#     "m2m:sub":{%s}
# }
# '''
#
#
# def which_payload(restype):
#     """Choose the correct payload header for each resource."""
#     restype = int(restype)
#     if restype == 2:
#         return ae_payload
#     elif restype == 3:
#         return cnt_payload
#     elif restype == 4:
#         return cin_payload
#     elif restype == 23:
#         return sub_payload
#     else:
#         return resourcepayload


def find_key(response, key):
    """Deserialize response, return value for key or None."""
    dic = response.json()
    key1 = list(dic.keys())
    key1 = sorted(key1, reverse=True)
    return dic.get(key1[0], None).get(key, None)


def getName(response):
    """Return the resource name in the response."""
    return find_key(response, "rn")


def getLastModifiedTime(response):
    """Return the lastModifiedTime in the response."""
    return find_key(response, "lt")


def getResid(response):
    """Return the resource id in the response."""
    return find_key(response, "ri")


def getParent(response):
    """Return the parent resource id in the response."""
    return find_key(response, "pi")


def getContent(response):
    """Return the content the response."""
    return find_key(response, "con")


def getRestype(response):
    """Return the resource type the response."""
    return find_key(response, "rty")


def getStatus(response):
    """Return the protocol status code in the response."""
    try:
        return response.status_code
    except(TypeError, AttributeError):
        return None


def getHeaders(response):
    """Return the protocol headers in the response."""
    try:
        return response.headers
    except(TypeError, AttributeError):
        return None


def getError(response):
    """Return the error string in the response."""
    try:
        return response.json()['error']
    except(TypeError, AttributeError):
        return None


def getNormalize(resourceURI):
    """Remove the first / of /InCSE1/ae1."""
    if resourceURI is not None:
        if resourceURI[0] == "/":
            return resourceURI[1:]
    return resourceURI



def reconf(server="localhost", base='InCSE1',
             auth=('admin', 'admin'), protocol="http"):
    """Connect to a IoTDM server."""
    session.auth = auth
    session.headers.update({'content-type': 'application/json'})
    payload = cse_payload % (base)
    server = "%s://" % (protocol) + server
    if base is not None:
        url = server + op_provision
        response = session.post(
            url, data=payload, timeout=timeout)
    return (response.status_code, response.text)

def create(resourceURI, restype, payload=None, name=None):
    """Create resource."""
    headers['X-M2M-NM'] = name
    headers['content-type'] = 'application/vnd.onem2m-res+json;ty=%s' % (restype)
    response = session.post(
        resourceURI, payload, timeout=timeout, headers=headers)
    return (response.status_code, response.text)

# def createWithCommand(parent, restype,
#                       command, attr=None, name=None):
#     """Create resource."""
#     payload = which_payload(restype)
#     payload = payload % (attr)
#     headers['X-M2M-NM'] = name
#     headers['content-type'] = 'application/vnd.onem2m-res+json;ty=%s' % (restype)
#     url = server + ":8282/%s?%s" % (
#         parent, command)
#     response = session.post(
#         url, payload, timeout=timeout, headers=headers)
#     return response

def retrieve(resourceURI):
    """Retrieve resource."""
    headers['content-type'] = 'application/vnd.onem2m-res+json'
    response = session.get(
        resourceURI, timeout=timeout, headers=headers
    )
    return (response.status_code, response.text)

# def retrieveWithCommand(resourceURI, command):
#     """Retrieve resource with command."""
#     if resourceURI is None:
#         return None
#     if command is None:
#         return None
#     resourceURI = normalize(resourceURI)
#     url = server + ":8282/%s?%s" % (resourceURI, command)
#     headers['X-M2M-NM'] = None
#     headers['content-type'] = 'application/vnd.onem2m-res+json'
#     response = session.get(
#         url, timeout=timeout, headers=headers
#     )
#     return response

def update(resourceURI, restype, attr=None):
    """Update resource attr."""
    payload = which_payload(restype)
    payload = payload % (attr)
    headers['content-type'] = 'application/vnd.onem2m-res+json'
    response = session.put(
        resourceURI, data=payload, timeout=timeout, headers=headers
    )
    return (response.status_code, response.text)

# def updateWithCommand(resourceURI, restype,
#                       command, attr=None, name=None):
#     """Update resource attr."""
#     if resourceURI is None:
#         return None
#     resourceURI = normalize(resourceURI)
#     payload = which_payload(restype)
#     payload = payload % (attr)
#     if name is None:
#         headers['X-M2M-NM'] = None
#     else:
#         headers['X-M2M-NM'] = name
#     headers['content-type'] = 'application/vnd.onem2m-res+json'
#     url = server + ":8282/%s?%s" % (resourceURI, command)
#     response = session.put(
#         url, payload, timeout=timeout, headers=headers)
#     return response

def delete(resourceURI):
    """Delete the resource with the provresourceURIed resourceURI."""
    headers['content-type'] = 'application/vnd.onem2m-res+json'
    response = session.delete(
        resourceURI, timeout=timeout, headers=headers
    )
    return (response.status_code, response.text)

# def deleteWithCommand(resourceURI, command):
#     """Delete the resource with the provresourceURIed resourceURI."""
#     if resourceURI is None:
#         return None
#     resourceURI = normalize(resourceURI)
#     url = server + ":8282/%s?%s" % (resourceURI, command)
#     headers['X-M2M-NM'] = None
#     headers['content-type'] = 'application/vnd.onem2m-res+json'
#     response = session.delete(url, timeout=timeout,
#                                         headers=headers)
#     return response

def tree():
    """Get the resource tree."""
    url = server + op_tree
    response = session.get(url)
    return response

def kill(server="localhost", auth=('admin', 'admin'), protocol="http"):
    """Kill the tree."""
    session.auth = auth
    session.headers.update({'content-type': 'application/json'})
    url = 'http://'+ server + op_cleanup
    response = session.post(url)
    return (response.status_code, response.text)
