#!/usr/bin/env python
from src.net import *
from src.arc import *
from src.ppl_wrapper import *
from src.integer_extended import *
import ppl




#Construction of a net from scratch
net = Net("0",3,3,2)
print("##### INTIAL TESTS #######")
print("net without arcs:\n%s" % net)
i1 = Arc("i1",LinearExpressionExtended(net.params[0] + net.params[1] -2),net.places[0],net.transitions[0])
o1 = Arc("o1",LinearExpressionExtended(1),net.transitions[0],net.places[1])
i2 = Arc("i2",LinearExpressionExtended(1),net.places[1],net.transitions[1])
o2 = Arc("o2",LinearExpressionExtended(net.params[1]),net.transitions[1],net.places[2])
i3 = Arc("i3",LinearExpressionExtended(1),net.places[2],net.transitions[2])
o3 = Arc("o3",LinearExpressionExtended(1),net.transitions[2],net.places[1])
print("net with arcs:\n%s" % net) #TODO ADD THE ARCS ?
net.initialize_constraint_system()
net.compute_pre_matrix()
net.compute_post_matrix()

#Test of str methods for several classes
print("\n##### DISPLAY METHODS #########")
print(net.places[0].get_tokens())
print(o2)
print("\n".join(map(str, net.transitions[1].get_pre())))
print("\n".join(map(str, net.transitions[1].get_post())))

#Test of the semantics
print("\n##### SEMANTICS #########")
net.places[0].add_tokens(LinearExpressionExtended(3))
print("m %s" %net.display_marking())
print(net.is_enabled(net.transitions[0]))
enabled = net.get_enabled_transitions()
print("firable transitions: %s" %str(enabled))
print(net.is_enabled(net.transitions[0]))

net.fire(net.transitions[0])
print("m0 -- t0 --> m1")

print("m %s" %net.display_marking())

enabled = net.get_enabled_transitions()
print("firable transitions: %s" %str(enabled))
net.fire(net.transitions[1])
print("m1 -- t1 --> m2")
print("m %s" %net.display_marking())

#Test of the export method, note that the marking is updated in the exported file
net.export_to_dot()

#test is_parametric methods
print("\n##### TEST PRESENCE OF PARAMETERS #########")
print("ARCS: \n Is input of t1 param ? %s\n is output of t1 param ?%s" %(i1.is_parametric(),o1.is_parametric()))
print("TRANSITION t1:\n Is t1 pre Param ? %s\nIs t1 Post Param ? %s\n Is t1 Param ? %s" % (net.transitions[0].is_parametric_pre(), net.transitions[0].is_parametric_post(), net.transitions[0].is_parametric()))
print("TRANSITION t3:\n Is t3 pre Param ? %s\nIs t3 Post Param ? %s\n Is t3 Param ? %s" % (net.transitions[2].is_parametric_pre(), net.transitions[2].is_parametric_post(), net.transitions[2].is_parametric()))

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
    enabled = train.get_enabled_transitions()
    print("firable transitions: %s" % str(enabled))
    #train.fire(train.transitions[0])
    train.export_to_dot()
else:
    print("Sorry, file xml/%s.xml does not exists" % fileName)

#Test Matrix
print("\n#### TEST PRE POST MATRICES #####")
print("Pre : %s" %str(net.Pre))
print("Post : %s" %str(net.Post))

#Dynamic Execution
print("\n#### TEST EXECUTION #####")
#net.execute()


#TEST TREES
import anytree
m0=net.marking()
enabled = net.get_enabled_transitions()
n1 = anytree.Node("root", m=net.marking(), t=None)
n2 = anytree.Node("leaf1", parent=n1, m=net.marking(),t=net.transitions[0])
n3 = anytree.Node("leaf2", parent=n1, m=net.marking(),t=net.transitions[1])
n4 = anytree.Node("leaf3", parent=n2, m=net.marking(),t=net.transitions[2])
n5 = anytree.Node("leaf4", parent=n4, m=net.marking(),t=net.transitions[0])
print(anytree.RenderTree(n1))
print(n4.anchestors.__class__.__name__)
import anytree.dotexport

def nodenamefunc(node):
    return '%s:%s' % (node.name, node.m)

def edgeattrfunc(node, child):
    return 'label="%s"' % (child.t)

anytree.dotexport.RenderTreeGraph(n1,nodenamefunc=nodenamefunc,nodeattrfunc=lambda node: "shape=box",edgeattrfunc=edgeattrfunc).to_picture("udo.png")

#Test evaluation of a net
print("\n#### TEST PRE EVALUATION #####")
net.evaluate({0: 1, 1: 2})
print("Pre : %s" %str(net.Pre))
print("Post : %s" %str(net.Post))
print("m %s" %net.marking())
net.export_to_dot()
m = [LinearExpressionExtended(0), LinearExpressionExtended(3), LinearExpressionExtended(1)]
m2 = [LinearExpressionExtended(0), LinearExpressionExtended(3), LinearExpressionExtended(0)]
print(net.is_enabled_from_marking(m,net.transitions[0]))
print(net.is_enabled_from_marking(m,net.transitions[1]))
print(net.is_enabled_from_marking(m,net.transitions[2]))
print(net.get_enabled_transitions_from_marking(m))
print(net.fire_from_marking(m,net.transitions[2]))
print(m)

net.build_KM_tree(m,100)

print(net.is_greater(m, m2))
m=net.accelerate(m, m2)
print(m)
print(net.get_enabled_transitions_from_marking(m))
print(net.get_enabled_transitions_from_marking(net.fire_from_marking(m,net.transitions[2])))



#Test Reachab
#net.build_partial_reach_tree(m,15)