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


def create(URI, resource_type, resource_name, payload):
    uri = urlparse(URI)
    if uri.scheme == "http":
        response = ciotdm.create(URI, resource_type, payload, resource_name)
        print str(response[0]) + '\n' + response[1]

    elif uri.scheme == "coap":
        log.startLogging(sys.stdout)
        endpoint = resource.Endpoint(None)
        protocol = coap.Coap(endpoint)
        Agent(protocol, "post", URI, payload=payload, ty=resource_type, nm=resource_name)
        reactor.listenUDP(0, protocol)
        reactor.run()

    else:
        print "Invalid protocol."
        sys.exit(2)

def retrieve(URI):
    uri = urlparse(URI)
    if uri.scheme == "http":
        response = ciotdm.retrieve(URI)
        print str(response[0]) + '\n' + response[1]

    elif uri.scheme == "coap":
        log.startLogging(sys.stdout)
        endpoint = resource.Endpoint(None)
        protocol = coap.Coap(endpoint)
        Agent(protocol, "get", URI)
        reactor.listenUDP(0, protocol)
        reactor.run()

    else:
        print "Invalid protocol."
        sys.exit(2)


def update(URI, resource_type, payload):
    uri = urlparse(URI)
    if uri.scheme == "http":
        response = ciotdm.update(URI, resource_type, payload)
        print str(response[0]) + '\n' + response[1]

    elif uri.scheme == "coap":
        log.startLogging(sys.stdout)
        endpoint = resource.Endpoint(None)
        protocol = coap.Coap(endpoint)
        Agent(protocol, "put", URI, payload=payload, ty=resource_type)
        reactor.listenUDP(0, protocol)
        reactor.run()

    else:
        print "Invalid protocol."
        sys.exit(2)

def delete(URI):
    uri = urlparse(URI)
    if uri.scheme == "http":
        response = ciotdm.delete(URI)
        print str(response[0]) + '\n' + response[1]

    elif uri.scheme == "coap":
        log.startLogging(sys.stdout)
        endpoint = resource.Endpoint(None)
        protocol = coap.Coap(endpoint)
        Agent(protocol, "delete", URI)
        reactor.listenUDP(0, protocol)
        reactor.run()

    else:
        print "Invalid protocol."
        sys.exit(2)
