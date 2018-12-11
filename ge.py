import networkx as nx

G = nx.Graph()

G.add_nodes_from([1,2,3])
G.add_edges_from([(1,2),(2,1),(2,3),(1,3)])

for u in G.edges_iter():
    print (u)

