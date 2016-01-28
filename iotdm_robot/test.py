import sys
from ciotdm import connect
from urlparse import urlparse
from txThings.examples.client import Agent
from twisted.internet import reactor
from twisted.python import log
import iotdm_robot.txThings.txthings.coap as coap
import iotdm_robot.txThings.txthings.resource as resource


'''to-do: payload serialisation'''

def restConf(URI, Cse_name, username, password):
    uri = urlparse(URI)
    connect(uri.netloc, Cse_name, (username, password))

def create(URI, resource_type, resource_name):
    uri = urlparse(URI)
    if uri.scheme == "http":
        response = connect.create(resource_type, name=resource_name)
        print response

    elif uri.scheme == "coap":
        log.startLogging(sys.stdout)
        endpoint = resource.Endpoint(None)
        protocol = coap.Coap(endpoint)
        Agent(protocol, "post", URI, resource_type, resource_name)
        reactor.listenUDP(0, protocol)
        reactor.run()

    else:
        print "Invalid protocol."
        sys.exit(2)

def retrieve(URI):
    uri = urlparse(URI)
    if uri.scheme == "http":
        pass

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


def update(URI):
    uri = urlparse(URI)
    if uri.scheme == "http":
        pass
        #response = connect.create(resource_type, name=resource_name)
        #print response

    elif uri.scheme == "coap":
        log.startLogging(sys.stdout)
        endpoint = resource.Endpoint(None)
        protocol = coap.Coap(endpoint)
        Agent(protocol, "put", URI, resource_type, resource_name)
        reactor.listenUDP(0, protocol)
        reactor.run()

    else:
        print "Invalid protocol."
        sys.exit(2)


#restConf('http://localhost', 'ODL-oneM2M-Cse', 'admin', 'admin')

#create("coap://127.0.0.1:5683/ODL-oneM2M-Cse/", 2, "AE3")

#retrieve("coap://127.0.0.1:5683/ODL-oneM2M-Cse")

update("coap://127.0.0.1:5683/ODL-oneM2M-Cse/AE1")