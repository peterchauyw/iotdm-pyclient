import sys
import ciotdm
from urlparse import urlparse
import json
from txThings.examples.client import Agent
from twisted.internet import reactor
from twisted.python import log
import txThings.txthings.coap as coap
import txThings.txthings.resource as resource

















def restConf(URI, Cse_name, username, password):
    uri = urlparse(URI)
    response = ciotdm.reconf(uri.netloc, Cse_name, (username, password))
    print str(response[0]) + '\n' + response[1]


def cleanup(URI, username, password):
    uri = urlparse(URI)
    response = ciotdm.kill(uri.netloc, (username, password))
    print str(response[0]) + '\n' + response[1]


def create(URI, resource_type, payload, origin=None, requestID=None):
    uri = urlparse(URI)
    if uri.scheme == "http":
        response = ciotdm.create(URI, resource_type, payload, origin, requestID)
        print str(response[0]) + '\n' + response[1]

    elif uri.scheme == "coap":
        log.startLogging(sys.stdout)
        endpoint = resource.Endpoint(None)
        protocol = coap.Coap(endpoint)
        Agent(protocol, "post", URI, payload=payload, ty=resource_type, origin=origin, requestID=requestID)
        reactor.listenUDP(0, protocol)
        reactor.run()

    else:
        print "Invalid protocol."
        sys.exit(2)

def retrieve(URI, origin=None, requestID=None):
    uri = urlparse(URI)
    if uri.scheme == "http":
        response = ciotdm.retrieve(URI, origin, requestID)
        print str(response[0]) + '\n' + response[1]

    elif uri.scheme == "coap":
        log.startLogging(sys.stdout)
        endpoint = resource.Endpoint(None)
        protocol = coap.Coap(endpoint)
        Agent(protocol, "get", URI, origin=origin, requestID=requestID)
        reactor.listenUDP(0, protocol)
        reactor.run()

    else:
        print "Invalid protocol."
        sys.exit(2)


def update(URI, payload, origin=None, requestID=None):
    uri = urlparse(URI)
    if uri.scheme == "http":
        response = ciotdm.update(URI, payload, origin, requestID)
        print str(response[0]) + '\n' + response[1]

    elif uri.scheme == "coap":
        log.startLogging(sys.stdout)
        endpoint = resource.Endpoint(None)
        protocol = coap.Coap(endpoint)
        Agent(protocol, "put", URI, payload=payload, origin=origin, requestID=requestID)
        reactor.listenUDP(0, protocol)
        reactor.run()

    else:
        print "Invalid protocol."
        sys.exit(2)

def delete(URI, origin=None, requestID=None):
    uri = urlparse(URI)
    if uri.scheme == "http":
        response = ciotdm.delete(URI, origin, requestID)
        print str(response[0]) + '\n' + response[1]

    elif uri.scheme == "coap":
        log.startLogging(sys.stdout)
        endpoint = resource.Endpoint(None)
        protocol = coap.Coap(endpoint)
        Agent(protocol, "delete", URI, origin=origin, requestID=requestID)
        reactor.listenUDP(0, protocol)
        reactor.run()

    else:
        print "Invalid protocol."
        sys.exit(2)
