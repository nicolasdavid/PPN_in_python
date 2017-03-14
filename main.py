#!/usr/bin/env python
from src.net import *
from src.arc import *
from src.ppl_wrapper import *
import ppl


net = Net("0",3,3,2)
print(net)
i1 = Arc("i1",ppl.Linear_Expression(net.params[0] + net.params[1] -2),net.places[0],net.transitions[0])
o1 = Arc("o1",ppl.Linear_Expression(1),net.transitions[0],net.places[1])
i2 = Arc("i2",ppl.Linear_Expression(1),net.places[1],net.transitions[1])
o2 = Arc("o2",ppl.Linear_Expression(net.params[1]),net.transitions[1],net.places[2])
i3 = Arc("i3",ppl.Linear_Expression(1),net.places[2],net.transitions[2])
o3 = Arc("o3",ppl.Linear_Expression(1),net.transitions[2],net.places[1])

print(net.places[0].getTokens())
print(o2)
print("\n".join(map(str,net.transitions[1].getPre())))
print("\n".join(map(str,net.transitions[1].getPost())))

print(net.display_marking())
net.places[0].addTokens(ppl.Linear_Expression(10))
print(net.display_marking())
net.fire(net.transitions[0])
print(net.display_marking())
net.fire(net.transitions[1])
print(net.display_marking())

print(net)

#test parametric
print("ARCS: \n Is input of t1 param ? %s\n is output of t1 param ?%s" %(i1.is_parametric(),o1.is_parametric()))
print("TRANSITION t1:\n Is t1 pre Param ? %s\nIs t1 Post Param ? %s\n Is t1 Param ? %s" %(net.transitions[0].isParametricPre(),net.transitions[0].isParametricPost(),net.transitions[0].is_parametric()))
print("TRANSITION t3:\n Is t3 pre Param ? %s\nIs t3 Post Param ? %s\n Is t3 Param ? %s" %(net.transitions[2].isParametricPre(),net.transitions[2].isParametricPost(),net.transitions[2].is_parametric()))

net.evaluate({ 1 : 5})

i1.get_param_present(net.params)

print("test subclass:\n")
print("is Pre ? %s" %(net.is_pre_parametric()))
print("is Post ? %s" %(net.is_post_parametric()))
print("is Distinct ? %s" %(net.is_distinct_parametric()))

