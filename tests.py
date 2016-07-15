import iotdm_api
from onem2m_xml_protocols.ae import ae
from onem2m_xml_protocols.container import cnt
from onem2m_xml_protocols.contentinstance import cin
from onem2m_xml_protocols.subscription import sub
from onem2m_xml_protocols.remotecse import csr
from onem2m_xml_protocols.acp import acp
from onem2m_xml_protocols.acp import acr
from onem2m_xml_protocols.group import grp
from onem2m_xml_protocols.node import nod
from onem2m_xml_protocols.firmware import fwr


'''RestConf call'''
# iotdm_api.restConf('http://localhost', 'ODL-oneM2M-Cse', 'admin', 'admin')

'''Cleanup call'''
# iotdm_api.cleanup('http://localhost', 'admin', 'admin')


'''AE Creation'''
# AE = ae()
# AE.set_api("TestAppId")
# AE.set_apn("testAppName")
# AE.set_or("http://ontology/ref")
# AE.set_rr(True)
# AE.set_rn("TestAE1")
# payload = AE.to_JSON()
# iotdm_api.create("http://localhost:8282/ODL-oneM2M-Cse", 2, payload, origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")


'''Container Creation'''
# container = cnt()
# container.set_mbs(30)
# container.set_or("http://hey/you")
# container.set_lbl(["key1"])
# container.set_rn("TestContainer")
# payload = container.to_JSON()
# iotdm_api.create("http://localhost:8282/ODL-oneM2M-Cse/TestAE", 3, payload)

'''Content-instance Creation'''
# subscription = sub()
# subscription.set_nu(["http://localhost"])
# subscription.set_rn("TestSubscription")
# payload  = subscription.to_JSON()
# iotdm_api.create("coap://localhost:5683/ODL-oneM2M-Cse/TestAE/TestContainer", 23, payload)


'''Subscription creation'''
# subscription = sub()
# subscription.set_nu(["10.195.131.12"])
# payload  = subscription.to_JSON()
# iotdm_api.create("coap://127.0.0.1:5683/ODL-oneM2M-Cse/AE/Container", 23, "sub1", payload)


'''Get'''
# iotdm_api.retrieve("http://localhost:8282/ODL-oneM2M-Cse?fu=1")


'''Delete'''
# iotdm_api.delete("http://127.0.0.1:8282/ODL-oneM2M-Cse/AE4")

'''Update'''
# AE = ae()
# AE.set_acpi(["ODL-oneM2M-Cse/TestAE/TestACP"])
# payload = AE.to_JSON()
# iotdm_api.update("coap://localhost:5683/ODL-oneM2M-Cse/TestAE", payload)


