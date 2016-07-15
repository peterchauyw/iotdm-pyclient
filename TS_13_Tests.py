import unittest
import iotdm_api

from onem2m_xml_protocols.ae import ae
from onem2m_xml_protocols.container import cnt
from onem2m_xml_protocols.contentinstance import cin
from onem2m_xml_protocols.subscription import sub
from onem2m_xml_protocols.remotecse import csr
from onem2m_xml_protocols.acp import acp
from onem2m_xml_protocols.group import grp
from onem2m_xml_protocols.node import nod
from onem2m_xml_protocols.firmware import fwr


class TS13(unittest.TestCase):
    def setUp(self):
        print "Setting up tests"

    def tearDown(self):
        print "Tearing down tests"

    def test_0_CSE_Provisioning(self):
        iotdm_api.restConf('http://localhost', 'ODL-oneM2M-Cse', 'admin', 'admin')

    def test_TD_M2M_NH_01_Retrieve_CSEBase(self):
        iotdm_api.retrieve("coap://localhost:5683/ODL-oneM2M-Cse", origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_NH_02_Create_RemoteCSE(self):
        remoteCSE = csr()
        remoteCSE.set_csi("//www.m2mprovider.com/CSE3219")
        remoteCSE.set_rr(True)
        remoteCSE.set_rn("RemoteCSE")
        payload = remoteCSE.to_JSON()
        iotdm_api.create("coap://localhost:5683/ODL-oneM2M-Cse", 16, payload, origin="//www.m2mprovider.com/CSE3219", requestID="12345")

    def test_TD_M2M_NH_03_Retrieve_RemoteCSE(self):
        iotdm_api.retrieve("coap://localhost:5683/ODL-oneM2M-Cse/RemoteCSE", origin="//www.m2mprovider.com/CSE3219", requestID="12345")

    def test_TD_M2M_NH_04_Update_RemoteCSE(self):
        remoteCSE = csr()
        payload = remoteCSE.to_JSON()
        iotdm_api.update("coap://localhost:5683/ODL-oneM2M-Cse", payload, origin="//www.m2mprovider.com/CSE3219", requestID="12345")

    def test_TD_M2M_NH_05_Delete_RemoteCSE(self):
        iotdm_api.delete("coap://localhost:5683/ODL-oneM2M-Cse/RemoteCSE", origin="//www.m2mprovider.com/CSE3219", requestID="12345")

    def test_TD_M2M_NH_06_Create_AE(self):
        AE = ae()
        AE.set_api("Nk836-t071-fc022")
        AE.set_rr(True)
        AE.set_rn("TestAE22")
        payload = AE.to_JSON()
        iotdm_api.create("coap://localhost:5683/ODL-oneM2M-Cse", 2, payload, origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_NH_07_Retrieve_AE(self):
        iotdm_api.retrieve("coap://localhost:5683/ODL-oneM2M-Cse/TestAE", origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_NH_08_Update_AE(self):
        AE = ae()
        AE.set_acpi(["ODL-oneM2M-Cse/TestAE/TestACP"])
        payload = AE.to_JSON()
        iotdm_api.update("coap://localhost:5683/ODL-oneM2M-Cse/TestAE", payload, origin="admin", requestID="12345")

    def test_TD_M2M_NH_09_Delete_AE(self):
        iotdm_api.delete("coap://localhost:5683/ODL-oneM2M-Cse/TestAE", origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_NH_10_Create_Container(self):
        container = cnt()
        container.set_rn("TestContainer")
        payload = container.to_JSON()
        iotdm_api.create("coap://localhost:5683/ODL-oneM2M-Cse/TestAE", 3, payload, origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_NH_11_Retrieve_Container(self):
        iotdm_api.retrieve("coap://localhost:5683/ODL-oneM2M-Cse/TestAE/TestContainer", origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_NH_12_Update_Container(self):
        container = cnt()
        payload = container.to_JSON()
        iotdm_api.update("coap://localhost:5683/ODL-oneM2M-Cse/TestAE/TestContainer", payload, origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_NH_13_Delete_Container(self):
        iotdm_api.delete("coap://localhost:5683/ODL-oneM2M-Cse/TestAE/TestContainer", origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_NH_14_Create_ContentInstance(self):
        con_instance = cin()
        con_instance.set_con("some data")
        con_instance.set_rn("TestContentInstance")
        payload = con_instance.to_JSON()
        iotdm_api.create("coap://localhost:5683/ODL-oneM2M-Cse/TestAE/TestContainer", 4, payload, origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_NH_15_Retrieve_ContentInstance(self):
        iotdm_api.retrieve("coap://localhost:5683/ODL-oneM2M-Cse/TestAE/TestContainer/TestContentInstance", origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_NH_17_Delete_ContentInstance(self):
        iotdm_api.delete("coap://localhost:5683/ODL-oneM2M-Cse/TestAE/TestContainer/TestContentInstance", origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_NH_18_Discovery_of_all_resources(self):
        iotdm_api.retrieve("coap://localhost:5683/ODL-oneM2M-Cse?fu=1", origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_NH_19_Discovery_with_label_filter_criteria(self):
        iotdm_api.retrieve("coap://localhost:5683/ODL-oneM2M-Cse?fu=1&lbl=key1", origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_NH_20_Discovery_with_limit_filter_criteria(self):
        iotdm_api.retrieve("coap://localhost:5683/ODL-oneM2M-Cse?fu=1&lim=2", origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_NH_21_Discovery_with_multiple_filter_criteria(self):
        iotdm_api.retrieve("coap://localhost:5683/ODL-oneM2M-Cse?fu=1&lbl=key1&lbl=key2", origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_NH_22_Create_Subscription(self):
        subscription = sub()
        subscription.set_nu(["http://localhost"])
        subscription.set_rn("TestSubscription")
        payload = subscription.to_JSON()
        iotdm_api.create("coap://localhost:5683/ODL-oneM2M-Cse/TestAE/TestContainer", 23, payload, origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_NH_23_Retrieve_Subscription(self):
        iotdm_api.retrieve("coap://localhost:5683/ODL-oneM2M-Cse/TestAE/TestContainer/TestSubscription", origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_NH_24_Update_Subscription(self):
        subscription = sub()
        payload = subscription.to_JSON()
        iotdm_api.update("coap://localhost:5683/ODL-oneM2M-Cse/TestAE/TestContainer/TestSubscription", payload, origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_NH_25_Delete_Subscription(self):
        iotdm_api.delete("coap://localhost:5683/ODL-oneM2M-Cse/TestAE/TestContainer/TestSubscription", origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_NH_26_Create_AccessControlPolicy(self):
        accessControlRule1 = acr()
        accessControlRule1.set_acor(["*"])
        accessControlRule1.set_acop(63)
        pv_payload = accessControlRule1.to_JSON()
        accessControlRule2 = acr()
        accessControlRule2.set_acor(["admin"])
        accessControlRule2.set_acop(63)
        pvs_payload = accessControlRule2.to_JSON()
        accessControlPolicy = acp()
        accessControlPolicy.set_pv(pv_payload)
        accessControlPolicy.set_pvs(pvs_payload)
        accessControlPolicy.set_rn("TestACP")
        payload = accessControlPolicy.to_JSON()
        iotdm_api.create("coap://localhost:5683/ODL-oneM2M-Cse/TestAE", 1, payload, origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_NH_27_Retrieve_AccessControlPolicy(self):
        iotdm_api.retrieve("coap://localhost:5683/ODL-oneM2M-Cse/TestAE/TestACP", origin="admin", requestID="12345")

    def test_TD_M2M_NH_28_Update_AccessControlPolicy(self):
        accessControlRule1 = acr()
        accessControlRule1.set_acor(["admin"])
        accessControlRule1.set_acop(63)
        pv_payload = accessControlRule1.to_JSON()
        accessControlRule2 = acr()
        accessControlRule2.set_acor(["admin"])
        accessControlRule2.set_acop(63)
        pvs_payload = accessControlRule2.to_JSON()
        accessControlPolicy = acp()
        accessControlPolicy.set_pv(pv_payload)
        accessControlPolicy.set_pvs(pvs_payload)
        accessControlPolicy.set_rn("TestACP")
        payload = accessControlPolicy.to_JSON()
        iotdm_api.update("coap://localhost:5683/ODL-oneM2M-Cse/TestAE/TestACP", payload, origin="admin", requestID="12345")

    def test_TD_M2M_NH_29_Delete_AccessControlPolicy(self):
        iotdm_api.delete("coap://localhost:5683/ODL-oneM2M-Cse/TestAE/TestACP", origin="admin", requestID="12345")

    #Insufficient Access Rights
    def test_TD_M2M_NH_30_Unauthorized_operation(self):
        iotdm_api.delete("coap://localhost:5683/ODL-oneM2M-Cse/TestAE/TestContainer", origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_NH_31_Create_Group(self):
        group = grp()
        group.set_mt(2)
        group.set_mnm(10)
        group.set_mid(["a"])
        group.set_rn("TestGroup")
        payload = group.to_JSON()
        iotdm_api.create("coap://localhost:5683/ODL-oneM2M-Cse", 9, payload, origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_NH_32_Retrieve_Group(self):
        iotdm_api.retrieve("coap://localhost:5683/ODL-oneM2M-Cse/TestGroup", origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_NH_33_Update_Group(self):
        group = grp()
        payload = group.to_JSON()
        iotdm_api.update("coap://localhost:5683/ODL-oneM2M-Cse/TestGroup", payload, origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_NH_34_Delete_Group(self):
        iotdm_api.delete("coap://localhost:5683/ODL-oneM2M-Cse/TestGroup", origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_NH_35_Create_Node(self):
        node = nod()
        node.set_ni("a")
        node.set_rn("TestNode")
        payload = node.to_JSON()
        iotdm_api.create("coap://localhost:5683/ODL-oneM2M-Cse", 14, payload, origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_NH_36_Retrieve_Node(self):
        iotdm_api.retrieve("coap://localhost:5683/ODL-oneM2M-Cse/TestNode", origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_NH_37_Update_Node(self):
        node = nod()
        payload = node.to_JSON()
        iotdm_api.update("coap://localhost:5683/ODL-oneM2M-Cse/TestNode", payload, origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_NH_38_Delete_Node(self):
        iotdm_api.delete("coap://localhost:5683/ODL-oneM2M-Cse/TestNode", origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_SH_05_Create_MgmtObj(self):
        firmware = fwr()
        firmware.set_mgd("1001")
        firmware.set_ud(True)
        firmware.set_vr("1")
        firmware.set_url("localhost")
        firmware.set_fwnnam("TestFirmware")
        firmware.set_rn("TestFirmware")
        payload = firmware.to_JSON()
        iotdm_api.create("coap://localhost:5683/ODL-oneM2M-Cse/TestNode", 13, payload, origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_SH_06_Update_MgmtObj(self):
        firmware = fwr()
        firmware.set_mgd("1001")
        firmware.set_ud(False)
        payload = firmware.to_JSON()
        iotdm_api.update("coap://localhost:5683/ODL-oneM2M-Cse/TestNode/TestFirmware", payload, origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_SH_07_Retrieve_MgmtObj(self):
        iotdm_api.retrieve("coap://localhost:5683/ODL-oneM2M-Cse/TestNode/TestFirmware", origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

    def test_TD_M2M_SH_08_Delete_MgmtObj(self):
        iotdm_api.delete("coap://localhost:5683/ODL-oneM2M-Cse/TestNode/TestFirmware", origin="//www.m2mprovider.com/CSE3219/C9886", requestID="12345")

if __name__ == '__main__':
    unittest.main()