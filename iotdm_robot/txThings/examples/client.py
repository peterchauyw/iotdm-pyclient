'''
Created on 08-09-2012

@author: Maciej Wasilak
'''

import sys
from urlparse import urlparse
from iotdm_robot import OneM2M

from twisted.internet.defer import Deferred
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from twisted.python import log

import iotdm_robot.txThings.txthings.coap as coap
import iotdm_robot.txThings.txthings.resource as resource


class Agent():
    """
    Example class which performs single PUT request to iot.eclipse.org
    port 5683 (official IANA assigned CoAP port), URI "/large-update".
    Request is sent 1 second after initialization.

    Payload is bigger than 64 bytes, and with default settings it
    should be sent as several blocks.
    """

    def __init__(self, protocol, op, uri, ty=None, nm=None):
        self.protocol = protocol
        self.ty = ty
        self.nm = nm
        self.uri = urlparse(uri)
        tmp = self.uri.netloc.split(':')
        self.host = tmp[0]
        self.path = self.uri.path.strip("/")
        self.query = self.uri.query
        if self.ty == None:
            self.payload = OneM2M.json_payload["update"]
        else:
            self.payload = OneM2M.json_payload[self.ty]
        if op == ("post" or "POST"):
            reactor.callLater(1, self.postResource)
        elif op == ("get" or "GET"):
            reactor.callLater(1, self.getResource)
        elif op == ("put" or "PUT"):
            reactor.callLater(1, self.putResource)
        elif op == ("delete" or "DELETE"):
            reactor.callLater(1, self.deleteResource)
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
        request.opt.oneM2M_FR = ("127.0.0.1",)
        request.opt.oneM2M_RQI = ("12345",)
        request.opt.oneM2M_NM = (self.nm,)
        request.opt.oneM2M_TY = self.ty
        request.remote = (self.host, coap.COAP_PORT)
        d = self.protocol.request(request)
        d.addCallback(self.printResponse)

    def getResource(self):

        request = coap.Message(code=coap.GET)
        request.opt.uri_path = (self.path,)
        request.opt.uri_query = (self.query,)
        request.opt.oneM2M_FR = ("127.0.0.1",)
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
        request.opt.oneM2M_FR = ("127.0.0.1",)
        request.opt.oneM2M_RQI = ("12345",)
        request.remote = (self.host, coap.COAP_PORT)
        d = self.protocol.request(request)
        d.addCallback(self.printResponse)


    def deleteResource(self):

        request = coap.Message(code=coap.DELETE)
        request.opt.uri_path = (self.path,)
        request.opt.oneM2M_FR = ("127.0.0.1",)
        request.opt.oneM2M_RQI = ("12345",)
        request.opt.observe = 0
        request.remote = (self.host, coap.COAP_PORT)
        d = self.protocol.request(request)
        d.addCallback(self.printResponse)
        d.addErrback(self.noResponse)

    def printResponse(self, response):
        print 'Response Code: ' + coap.responses[response.code]
        print 'Payload: ' + response.payload


    def noResponse(self, failure):
        print 'Failed to fetch resource:'
        print failure
        #reactor.stop()
