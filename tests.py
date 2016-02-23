import iotdm_api
from onem2m_xml_protocols.ae import ae
from onem2m_xml_protocols.container import cnt
from onem2m_xml_protocols.contentinstance import cin
from onem2m_xml_protocols.subscription import sub

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
# payload = AE.to_JSON()
# iotdm_api.create("coap://localhost:5683/ODL-oneM2M-Cse", 2, "AE10", payload)


'''Container Creation'''
# container = cnt()
# container.set_mbs(30)
# container.set_or("http://hey/you")
# container.set_lbl(["key1"])
# payload = container.to_JSON()
# iotdm_api.create("coap://10.195.131.10:5683/ODL-oneM2M-Cse/AE10", 3, "Container", payload)

'''Content-instance Creation'''
con_instance = cin()
con_instance.set_con("37")
payload = con_instance.to_JSON()
iotdm_api.create("http://10.195.131.12:8282/ODL-oneM2M-Cse/AE10/Container", 4, "Instance", payload)


'''Subscription creation'''
# subscription = sub()
# subscription.set_nu(["10.195.131.12"])
# payload  = subscription.to_JSON()
# iotdm_api.create("coap://127.0.0.1:5683/ODL-oneM2M-Cse/AE/Container", 23, "sub1", payload)


'''Get'''
# iotdm_api.retrieve("http://10.195.131.10:8282/ODL-oneM2M-Cse?fu=1")


'''Delete'''
# iotdm_api.delete("http://127.0.0.1:8282/ODL-oneM2M-Cse/AE4")