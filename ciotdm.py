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

def create(resourceURI, restype, payload=None, origin=None, requestID=None):
    """Create resource."""
    headers['content-type'] = 'application/vnd.onem2m-res+json;ty=%s' % (restype)
    if origin is not None:
        headers['X-M2M-Origin'] = origin
    if requestID is not None:
        headers['X-M2M-RI'] = requestID
    response = session.post(
        resourceURI, payload, timeout=timeout, headers=headers)
    return (response.status_code, response.text)

def retrieve(resourceURI, origin=None, requestID=None):
    """Retrieve resource."""
    headers['content-type'] = 'application/vnd.onem2m-res+json'
    if origin is not None:
        headers['X-M2M-Origin'] = origin
    if requestID is not None:
        headers['X-M2M-RI'] = requestID
    response = session.get(
        resourceURI, timeout=timeout, headers=headers
    )
    return (response.status_code, response.text)

def update(resourceURI, payload=None, origin=None, requestID=None):
    """Update resource attr."""
    headers['content-type'] = 'application/vnd.onem2m-res+json'
    if origin is not None:
        headers['X-M2M-Origin'] = origin
    if requestID is not None:
        headers['X-M2M-RI'] = requestID
    response = session.put(
        resourceURI, data=payload, timeout=timeout, headers=headers
    )
    return (response.status_code, response.text)

def delete(resourceURI, origin=None, requestID=None):
    """Delete the resource with the provresourceURIed resourceURI."""
    headers['content-type'] = 'application/vnd.onem2m-res+json'
    if origin is not None:
        headers['X-M2M-Origin'] = origin
    if requestID is not None:
        headers['X-M2M-RI'] = requestID
    response = session.delete(
        resourceURI, timeout=timeout, headers=headers
    )
    return (response.status_code, response.text)

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
