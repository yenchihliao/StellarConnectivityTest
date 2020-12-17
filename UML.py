from graphviz import Digraph as D

g = D('FBA_Exp', filename='graph.png')

g.attr(rankdir='LR')
g.attr('node', shape='record')
g.attr('edge', arrowhead='vee')

g.node('System')
g.node('N')
g.node('NFac')
g.node('Msg')
g.node('Timeout')
g.node('Conn')
g.node('Quorum')
g.node('Delay')

g.edge('System', 'N')
g.edge('N', 'NFac')
g.edge('N', 'Msg')
g.edge('NFac', 'Timeout')
g.edge('NFac', 'Conn')
g.edge('NFac', 'Quorum')
g.edge('Conn', 'Delay')

print(g.source)
g.view()
