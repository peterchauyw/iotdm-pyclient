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


# RestConf calls require admin access
iotdm_api.restConf('http://localhost', 'InCSE1', 'admin', 'admin')

# Clean-up of resource tree
iotdm_api.cleanup('http://localhost', 'admin', 'admin')


# CoAP Creation of an AE named "myAE" under the CSE base "InCSE1".
AE = ae()
AE.set_api("Nk836-t071-fc022")
AE.set_rr(True)
AE.set_rn("myAE")
payload = AE.to_JSON()
iotdm_api.create("coap://localhost:5683/InCSE1", 2, payload, origin="AE-ID", requestID="12345")


# Creation of a Container named "mySubContainer" with a maximum number of instances of 5, under "myContainer".
container = cnt()
container.set_rn("mySubContainer")
container.set_mni(5)
payload = container.to_JSON()
iotdm_api.create("http://localhost:8282/InCSE1/myAE/myContainer", 3, payload, origin="AE-ID", requestID="12345")


# Creation of a Content Instance named "myOtherContentInstance" under "mySubContainer", with "world" as its content.
con_instance = cin()
con_instance.set_con("world")
con_instance.set_rn("myOtherContentInstance")
payload = con_instance.to_JSON()
iotdm_api.create("http://localhost:8282/InCSE1/myAE/myContainer/mySubContainer", 4, payload, origin="AE-ID", requestID="12345")


# Update of the Container "mySubContainer", with its attribute "label" being set to "submarine"
container = cnt()
container.set_lbl(["submarine"])
payload = container.to_JSON()
iotdm_api.update("http://localhost:8282/InCSE1/myAE/myContainer/mySubContainer", payload, origin="AE-ID", requestID="12345")

# Deletion of the ContentInstance "myContentInstance"
iotdm_api.delete("http://localhost:8282/InCSE1/myAE/myContainer/myContentInstance", origin="AE-ID", requestID="12345")


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
