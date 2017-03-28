#!/usr/bin/env python
from src.net import *
from src.arc import *
from src.ppl_wrapper import *
from src.integer_extended import *
import ppl
import numpy
import networkx as nx
import matplotlib.pyplot as plt


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

#Test evaluation of a net
#net.evaluate({1: 5})

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
print("Pre : %s" %str(net.compute_pre_matrix()))
print("Post : %s" %str(net.compute_post_matrix()))

#Dynamic Execution
print("\n#### TEST EXECUTION #####")
net.execute()


#TEST TREES

#DRAW TREES

import graphviz as gv
import functools
graph = functools.partial(gv.Graph, format='png')
digraph = functools.partial(gv.Digraph, format='png')

def add_nodes(graph, nodes):
    for n in nodes:
        if isinstance(n, tuple):
            graph.node(n[0], **n[1])
        else:
            graph.node(n)
    return graph

def add_edges(graph, edges):
    for e in edges:
        if isinstance(e[0], tuple):
            graph.edge(*e[0], **e[1])
        else:
            graph.edge(*e)
    return graph

add_edges(
    add_nodes(digraph(), [
        ('A', {'label': 'Node A'}),
        ('B', {'label': 'Node B'}),
        'C'
    ]),
    [
        (('A', 'B'), {'label': 'Edge 1'}),
        (('A', 'C'), {'label': 'Edge 2'}),
        ('B', 'C')
    ]
).render('img/g5')

#ANALYZE TREES
try:
    import pygraphviz
    from networkx.drawing.nx_agraph import write_dot
    print("using package pygraphviz")
except ImportError:
    try:
        import pydotplus
        from networkx.drawing.nx_pydot import write_dot
        print("using package pydotplus")
    except ImportError:
        print()
        print("Both pygraphviz and pydotplus were not found ")
        print("see http://networkx.github.io/documentation"
              "/latest/reference/drawing.html for info")
        print()
        raise

G1=nx.DiGraph()
G1.add_node(0, label=net.marking())
G1.add_edge("n0","n10",label="t0")
G1.add_edge("n10","n20",label="t1")
print(G1.predecessors("n20"))
write_dot(G1,"test.dot")
