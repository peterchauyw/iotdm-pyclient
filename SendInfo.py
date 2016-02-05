#!/usr/bin/python

import criotdm
import ciotdm
import psutil
import threading

# Set varibles
httphost = "10.195.70.69"
httpuser = "admin"
httppass = "admin"
rt_ae              = 2
rt_container       = 3
rt_contentInstance = 4
rt_subscription = 23


connection1 = criotdm.connect_to_iotdm(httphost, httpuser, httppass, "http")
cntattr = '"mni"'

def sendCnt():
    threading.Timer(1.0,sendCnt).start()
    cpu = psutil.cpu_percent(interval=None)
    attr = cntattr + ":" + '\"%s\"' %(cpu)
    print cntattr
    container_resp = criotdm.create_resource(connection1,"ODL-oneM2M-Cse",rt_container,attr, "Container1")
    print container_resp


'''
# Create Container
attr = '"mni":30'
container_resp = criotdm.create_resource(connection1,"ODL-oneM2M-Cse",rt_container,attr, "Container1")
print(container_resp.text)

'''


sendCnt()


