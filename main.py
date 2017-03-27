#!/usr/bin/env python
from src.net import *
from src.arc import *
from src.ppl_wrapper import *
from src.integer_extended import *
import ppl
import numpy
import networkx as nx


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
print(net.places[0].get_tokens())
print(o2)
print("\n".join(map(str, net.transitions[1].get_pre())))
print("\n".join(map(str, net.transitions[1].get_post())))

#Test of the semantics
print("\n##### SEMANTICS #########")
print(net.display_marking())
net.places[0].add_tokens(ppl.Linear_Expression(10))
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
print("TRANSITION t1:\n Is t1 pre Param ? %s\nIs t1 Post Param ? %s\n Is t1 Param ? %s" % (net.transitions[0].is_parametric_pre(), net.transitions[0].is_parametric_post(), net.transitions[0].is_parametric()))
print("TRANSITION t3:\n Is t3 pre Param ? %s\nIs t3 Post Param ? %s\n Is t3 Param ? %s" % (net.transitions[2].is_parametric_pre(), net.transitions[2].is_parametric_post(), net.transitions[2].is_parametric()))

#Test evaluation of a net
net.evaluate({1: 5})

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

#Test Integer Extended
a = IntegerExtended()
print(a)
b = IntegerExtended(10)
print(b)
c = IntegerExtended(value=11)
print(c)
d = IntegerExtended(value=1, infinite=True)
print(d)
e = IntegerExtended(infinite=True)
print(e)
print(a*b)
print(a*e)

print(b+e)
print(b-e)
print(e-b)

t1 = numpy.array([a,b])
t2 = numpy.array([a,e])
t3 = t1+t2
print(t1 < t2)

u = LinearExpressionExtended(value=ppl.Linear_Expression(1), infinite=False)
v = LinearExpressionExtended(value=ppl.Linear_Expression(3), infinite=True)
print(u <= v)
print(v <= u)
print(v*2)

