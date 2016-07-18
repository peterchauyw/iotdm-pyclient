'''
Created on 08-09-2012

@author: Maciej Wasilak

Modified on 01-07-2016

@by: Peter Chau
'''

import sys
from urlparse import urlparse
import OneM2M
import socket
from twisted.internet import reactor
import txThings.txthings.coap as coap
# from twisted.internet.defer import Deferred
# from twisted.internet.protocol import DatagramProtocol
# from twisted.python import log
# import txThings.txthings.resource as resource


class Agent():

    def __init__(self, protocol, op, uri, payload=None, ty=None, origin=None, requestID=None):
        self.protocol = protocol
        self.ty = ty
        self.uri = urlparse(uri)
        tmp = self.uri.netloc.split(':')
        self.host = socket.gethostbyname(tmp[0])
        self.path = self.uri.path.strip("/")
        self.query = self.uri.query
        self.payload = payload
        self.origin = origin
        self.requestID = requestID
        if op == "post":
            reactor.callLater(0, self.postResource)
        elif op == "get":
            reactor.callLater(0, self.getResource)
        elif op == "put":
            reactor.callLater(0, self.putResource)
        elif op == "delete":
            reactor.callLater(0, self.deleteResource)
        else:
            print "Invalid operation"
            sys.exit(2)

    def postResource(self):

        request = coap.Message(code=coap.POST, payload=self.payload)
        request.opt.uri_host = (self.host,)
        request.opt.uri_port = int(self.uri.port)
        request.opt.uri_query = ("ty="+str(self.ty),)
        request.opt.uri_path = (self.path,)
        request.opt.content_format = coap.media_types_rev['application/json']
        if self.origin is not None:
            request.opt.oneM2M_FR = (self.origin,)
        else:
            request.opt.oneM2M_FR = ("//localhost:10000",)
        if self.requestID is not None:
            request.opt.oneM2M_RQI = (self.requestID,)
        else:
            request.opt.oneM2M_RQI = ("12345",)
        request.opt.oneM2M_TY = self.ty
        request.remote = (self.host, coap.COAP_PORT)
        d = self.protocol.request(request)
        d.addCallback(self.printResponse)
        d.addErrback(self.noResponse)


    def getResource(self):

        request = coap.Message(code=coap.GET)
        request.opt.uri_path = (self.path,)
        request.opt.uri_query = (self.query,)
        if self.origin is not None:
            request.opt.oneM2M_FR = (self.origin,)
        else:
            request.opt.oneM2M_FR = ("//localhost:10000",)
        if self.requestID is not None:
            request.opt.oneM2M_RQI = (self.requestID,)
        else:
            request.opt.oneM2M_RQI = ("12345",)
        request.opt.observe = 0
        request.remote = (self.host, coap.COAP_PORT)
        d = self.protocol.request(request)
        d.addCallback(self.printResponse)
        d.addErrback(self.noResponse)


    def putResource(self):

        request = coap.Message(code=coap.PUT, payload=self.payload)
        request.opt.uri_host = (self.host,)
        request.opt.uri_port = int(self.uri.port)
        request.opt.uri_path = (self.path,)
        request.opt.content_format = coap.media_types_rev['application/json']
        if self.origin is not None:
            request.opt.oneM2M_FR = (self.origin,)
        else:
            request.opt.oneM2M_FR = ("//localhost:10000",)
        if self.requestID is not None:
            request.opt.oneM2M_RQI = (self.requestID,)
        else:
            request.opt.oneM2M_RQI = ("12345",)
        request.remote = (self.host, coap.COAP_PORT)
        d = self.protocol.request(request)
        d.addCallback(self.printResponse)
        d.addErrback(self.noResponse)


    def deleteResource(self):

        request = coap.Message(code=coap.DELETE)
        request.opt.uri_path = (self.path,)
        if self.origin is not None:
            request.opt.oneM2M_FR = (self.origin,)
        else:
            request.opt.oneM2M_FR = ("//localhost:10000",)
        if self.requestID is not None:
            request.opt.oneM2M_RQI = (self.requestID,)
        else:
            request.opt.oneM2M_RQI = ("12345",)
        request.opt.observe = 0
        request.remote = (self.host, coap.COAP_PORT)
        d = self.protocol.request(request)
        d.addCallback(self.printResponse)
        d.addErrback(self.noResponse)


    def gotIP(ip):
        return ip
        reactor.callLater(0, reactor.stop)


    def printResponse(self, response):
        print 'Response Code: ' + coap.responses[response.code]
        print 'Payload: ' + response.payload
        reactor.stop()


    def noResponse(self, failure):
        print 'Failed to fetch resource:'
        print failure
        reactor.stop()
