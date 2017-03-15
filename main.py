#!/usr/bin/env python
from src.net import *
from src.arc import *
from src.ppl_wrapper import *
import ppl
from src.marking import *


#Construction of a net from scratch
net = Net("0",3,3,2)
print("##### INTIAL TESTS #######")
print("net without arcs:\n%s" % net)
i1 = Arc("i1",ppl.Linear_Expression(net.params[0] + net.params[1] -2),net.places[0],net.transitions[0])
o1 = Arc("o1",ppl.Linear_Expression(1),net.transitions[0],net.places[1])
i2 = Arc("i2",ppl.Linear_Expression(1),net.places[1],net.transitions[1])
o2 = Arc("o2",ppl.Linear_Expression(net.params[1]),net.transitions[1],net.places[2])
i3 = Arc("i3",ppl.Linear_Expression(1),net.places[2],net.transitions[2])
o3 = Arc("o3",ppl.Linear_Expression(1),net.transitions[2],net.places[1])
print("net with arcs:\n%s" % net) #TODO ADD THE ARCS ?

#Test of str methods for several classes
print("\n##### DISPLAY METHODS #########")
print(net.places[0].getTokens())
print(o2)
print("\n".join(map(str,net.transitions[1].getPre())))
print("\n".join(map(str,net.transitions[1].getPost())))

#Test of the semantics
print("\n##### SEMANTICS #########")
print(net.display_marking())
net.places[0].addTokens(ppl.Linear_Expression(10))
print(net.display_marking())
net.fire(net.transitions[0])
print(net.display_marking())
net.fire(net.transitions[1])
print(net.display_marking())

#Test of the export method, note that the marking is updated in the exported file
net.export_to_dot()

#test is_parametric methods
print("\n##### TEST PRESENCE OF PARAMETERS #########")
print("ARCS: \n Is input of t1 param ? %s\n is output of t1 param ?%s" %(i1.is_parametric(),o1.is_parametric()))
print("TRANSITION t1:\n Is t1 pre Param ? %s\nIs t1 Post Param ? %s\n Is t1 Param ? %s" %(net.transitions[0].isParametricPre(),net.transitions[0].isParametricPost(),net.transitions[0].is_parametric()))
print("TRANSITION t3:\n Is t3 pre Param ? %s\nIs t3 Post Param ? %s\n Is t3 Param ? %s" %(net.transitions[2].isParametricPre(),net.transitions[2].isParametricPost(),net.transitions[2].is_parametric()))

#Test evaluation of a net
net.evaluate({1: 5})
net.export_to_dot()

#Test get params of an arc
i1.get_param_present(net.params)

#Test type of net
print("\n#####test subclass#######")
print("exact subclass is: %s" %net.get_type_of_net())
print("is Pre ? %s" %(net.is_pre_parametric()))
print("is Post ? %s" %(net.is_post_parametric()))
print("is Distinct ? %s" %(net.is_distinct_parametric()))

#Test xml import
print("\n#### TEST XML IMPORT #####")
fileName = "train1"
if os.path.isfile("xml/%s.xml" % fileName):
    train = NetFromRomeoXML(fileName, 0)
    train.fire(train.transitions[0])
    train.export_to_dot()
else:
    print("Sorry, file xml/%s.xml does not exists" % fileName)


#Test Marking
m1 = Marking(3)
m1.set_omega([True, False, False])
m1.set_value([1, 2, 3])

m2 = Marking(3)
m2.set_omega([False, False, False])
m2.set_value([1, 2, 3])

m3 = Marking(3)
m3.set_omega([True, False, False])
m3.set_value([1, 4, 2])

print("markings:\nm1=%s\nm2=%s\nm3=%s" %(m1, m2, m3))
print(m1 < m2)
print(m2 < m1)
print(m1 < m3)
print(m3 < m1)

m = net.formal_marking()
print(m)
Pre = net.get_pre_matrix()
Post = net.get_post_matrix()
print("Pre: %s" % Pre)
print("Post: %s" % Post)

u = m - Pre[1]
print(u)
