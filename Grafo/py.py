import networkx as nx

G = nx.Graph()
G.add_nodes_from([1,2,3,4],valido = False)
G.add_edges_from([(1,2),(1,3),(1,4),(2,3),(2,4),(3,4)])
G[1][2]["distancia"] = 5
G[1][3]["distancia"] = 6
G[1][4]["distancia"] = 4
G[2][3]["distancia"] = 3
G[2][4]["distancia"] = 5
G[3][4]["distancia"] = 7

a = [1,2,3]
for u,v in G.edges_iter(1):
    print (u,v)

