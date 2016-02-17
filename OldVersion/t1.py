#!/usr/bin/env python
import ddm
c = ddm.connect("localhost:8282", proto="http")

#id = "InCSE1/10028/20020/30019"
#x=c.retrieve(id)
#x=c.update(id, {"contents": "bozo"})

ae = ddm.id(c.create("InCSE1", "AE"))
co = ddm.id(c.create(ae, "container"))
ci = ddm.id(c.create(co, "contentInstance", {"content": "102"}))

print "ae", ae
print "co", co
print "ci", ci

def huh(x):
	if x == None:
		print "c.error", c.error
	else:
		print "x", x

x = c.update(ae, {"labels":"100"})
huh(x)

x = c.update(co, {"labels":"101"})
huh(x)

x = c.retrieve(ci)
huh(x)
