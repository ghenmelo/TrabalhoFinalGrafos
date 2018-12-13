import networkx as nx
from modelo.veiculo import Veiculo

def TSP (G,veiculo):
    listaDeVertices = []
    verticeInicial = None
    i = 0
    for vertice in G.nodes_iter():
        listaDeVertices.append(vertice)
        if i == 0:
            verticeInicial = vertice
        i =+ 1

    listaDeVisitados = [listaDeVertices[0]]
    somaVolume = 0
    somaDinheiro = 0
    caminho = [listaDeVertices[0]]
    while len(listaDeVisitados) != len(listaDeVertices) and somaVolume <= veiculo.V and somaDinheiro <= veiculo.P:
        G,listaDeVisitados =  fun (G,listaDeVisitados)
        for i in listaDeVisitados:
            somaDinheiro += G[i]["dinheiro"]
            somaVolume += G[i]["volume"]
    for u,v in G.adjacency_iter():
        if G[u][v]["caminho"] == True :
            if u != listaDeVisitados[0]:
                G.remove_node(u)
                caminho.append(u)
            if v != listaDeVisitados[0]:
                G.remove_node(v)
                caminho.append(v)
    
    return G,caminho

def fun (G,listaVerticesVisitadas):

    melhorDistancia = float("inf")
    melhorAresta = (-1,-1)
    for u in listaVerticesVisitadas:
        for x,verticeAdjacente in G.edges_iter(u):
            if G[u][verticeAdjacente]["distancia"] < melhorDistancia and G.node[verticeAdjacente]["visitado"] == False and verticeAdjacente not in listaVerticesVisitadas :
                melhorDistancia = G[u][verticeAdjacente]["distancia"]
                melhorAresta = (u,verticeAdjacente)
    
    if len(listaVerticesVisitadas) == 1:
        G[melhorAresta[0]][melhorAresta[1]]["caminho"] = True
    elif len(listaVerticesVisitadas) == 2:
        G[melhorAresta[1]][listaVerticesVisitadas[0]]["caminho"] = True
        G[melhorAresta[1]][listaVerticesVisitadas[1]]["caminho"] = True
    else:
        novaMelhorDistancia = float("inf")
        novaMelhorAresta = (-1,-1)
        for u in listaVerticesVisitadas:
            for x,verticeAdjacente in G.edges_iter(u):
                if G[u][verticeAdjacente]["distancia"] < novaMelhorDistancia and melhorAresta[0] != u and verticeAdjacente == melhorAresta[1] :
                    novaMelhorDistancia = G[u][verticeAdjacente]["distancia"]
                    novaMelhorAresta = (u,verticeAdjacente)


        G[melhorAresta[0]][melhorAresta[1]]["caminho"] = True
        G[melhorAresta[0]][novaMelhorAresta[0]]["caminho"] = False
        G[novaMelhorAresta[0]][novaMelhorAresta[1]]["caminho"] = True
    listaVerticesVisitadas.append(melhorAresta[1])
    return G,listaVerticesVisitadas

def teste (veiculos):
    G = nx.Graph()
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

    N = nx.Graph()
    N = G
    caminhos = []
    i = 0
    melhorVeiculo = veiculos[0]
    
    while N.size() != 0:
        caminhoAtual = []
        for veiculo in veiculos:
            if veiculo.calculaCustoBeneficio() > melhorVeiculo.calculaCustoBeneficio():
                if veiculo.Nv != 0 :
                   melhorVeiculo = veiculo
        G,caminhoAtual = TSP(G,melhorVeiculo)
        caminhos[i] = {i+1:caminhoAtual}
        i += 1
        veiculos[veiculos.index(melhorVeiculo)].Nv -= veiculos[veiculos.index(melhorVeiculo)].Nv
    return caminhos


                
        

    # print ("resultado")
    #     soma = 0
    #     for u,v in G.edges_iter():
    #         if(G[u][v]["caminho"] == True):
    #             soma += G[u][v]["distancia"]
    #             print (u,v)
    #     print (soma)
veiculos = []
teste(veiculos)
        




    

    
        
        
            


            

        






