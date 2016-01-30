import sys
import ciotdm
from urlparse import urlparse
from txThings.examples.client import Agent
from twisted.internet import reactor
from twisted.python import log
import iotdm_robot.txThings.txthings.coap as coap
import iotdm_robot.txThings.txthings.resource as resource


'''to-do: payload serialisation'''

def restConf(URI, Cse_name, username, password):
    uri = urlparse(URI)
    response = ciotdm.reconf(uri.netloc, Cse_name, (username, password))
    print str(response[0]) + '\n' + response[1]


def cleanup(URI, username, password):
    uri = urlparse(URI)
    response = ciotdm.kill(uri.netloc, (username, password))
    print str(response[0]) + '\n' + response[1]


def create(URI, resource_type, resource_name):
    uri = urlparse(URI)
    if uri.scheme == "http":
        attr = '"api":"testAppId", "apn":"testAppName", "or":"http://ontology/ref","rr":true'
        response = ciotdm.create(URI, resource_type, attr, resource_name)
        print str(response[0]) + '\n' + response[1]

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


def update(URI, resource_type, attribute):
    uri = urlparse(URI)
    if uri.scheme == "http":
        response = ciotdm.update(URI, resource_type, attribute)
        print str(response[0]) + '\n' + response[1]

    elif uri.scheme == "coap":
        log.startLogging(sys.stdout)
        endpoint = resource.Endpoint(None)
        protocol = coap.Coap(endpoint)
        Agent(protocol, "put", URI)
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


#restConf('http://localhost', 'ODL-oneM2M-Cse', 'admin', 'admin')

#cleanup('http://localhost', 'admin', 'admin')

#create("http://127.0.0.1:8282/ODL-oneM2M-Cse/AE1", 2, "AE")

#retrieve("http://127.0.0.1:8282/ODL-oneM2M-Cse?fu=1")

#update("http://127.0.0.1:8282/ODL-oneM2M-Cse/AE3", 2, '"apn":"testAppName", "or":"http://ontology/ref","rr":true')

#delete("http://127.0.0.1:8282/ODL-oneM2M-Cse/AE4")