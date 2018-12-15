import networkx as nx

G = nx.Graph()
G.add_node(1,Silvia=69)
G.add_nodes_from([1,2,3,4,5],visitado = False,dinheiro = 0,volume = 0)
G.add_edges_from([(1,2),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5),(3,4),(3,5),(4,5)],caminho = False)
G[1][2]["distancia"] = 2
G[1][3]["distancia"] = 6
G[1][4]["distancia"] = 4
G[1][5]["distancia"] = 1
G[2][3]["distancia"] = 7
G[2][4]["distancia"] = 3
G[2][5]["distancia"] = 5
G[3][4]["distancia"] = 8
G[3][5]["distancia"] = 4
G[4][5]["distancia"] = 2

G.node[1]["dinheiro"] = 100
G.node[2]["dinheiro"] = 200
G.node[3]["dinheiro"] = 300
G.node[4]["dinheiro"] = 150
G.node[5]["dinheiro"] = 50

G.node[1]["volume"] = 10
G.node[2]["volume"] = 20
G.node[3]["volume"] = 30
G.node[4]["volume"] = 15
G.node[5]["volume"] = 5

a = {}
print (a)