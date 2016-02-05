'''
Created on 08-09-2012

@author: Maciej Wasilak
'''

import sys

from twisted.internet.defer import Deferred
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from twisted.python import log

import iotdm_robot.txThings.txthings.coap as coap
import iotdm_robot.txThings.txthings.resource as resource


class Agent():
    """
    Example class which performs single GET request to iot.eclipse.org
    port 5683 (official IANA assigned CoAP port), URI "obs".
    Request is sent 1 second after initialization.
    
    Remote IP address is hardcoded - no DNS lookup is preformed.

    Method requestResource constructs the request message to
    remote endpoint. Then it sends the message using protocol.request().
    A deferred 'd' is returned from this operation.

    Deferred 'd' is fired internally by protocol, when complete response is received.

    Method printResponse is added as a callback to the deferred 'd'. This
    method's main purpose is to act upon received response (here it's simple print).
    """

    def __init__(self, protocol):
        self.protocol = protocol
        reactor.callLater(1, self.requestResource)

    def requestResource(self):
        request = coap.Message(code=coap.GET)
        #Send request to "coap://iot.eclipse.org:5683/obs"
        request.opt.uri_path = ('ODL-oneM2M-Cse',)
        request.opt.observe = 0
        request.opt.oneM2M_FR = ("127.0.0.1",)
        request.opt.oneM2M_RQI = ("12345",)
        request.opt.uri_query = ("fu=1",)
        request.remote = ("127.0.0.1", coap.COAP_PORT)
        d = protocol.request(request, observeCallback=self.printLaterResponse)
        d.addCallback(self.printResponse)
        d.addErrback(self.noResponse)

    def printResponse(self, response):
        print 'First result: ' + response.payload
        #reactor.stop()

    def printLaterResponse(self, response):
        print 'Observe result: ' + response.payload

    def noResponse(self, failure):
        print 'Failed to fetch resource:'
        print failure
        #reactor.stop()

log.startLogging(sys.stdout)

endpoint = resource.Endpoint(None)
protocol = coap.Coap(endpoint)
client = Agent(protocol)

reactor.listenUDP(0, protocol)
reactor.run()
