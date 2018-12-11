import networkx as nx

def TSP ():
    G = nx.Graph()
    listaDeVertices = []
    verticeInicial = None
    i = 0
    for u,v in G.adjacency_iter():
        G[u]["visitado"] = False
        G[u][v]["caminho"] = False

    fun (G,listaDeVisitados)

    for vertice in G.nodes_iter():
        listaDeVertices[i].append(vertice)
        if i == 0:
            verticeInicial = vertice
        i =+ 1

    listaDeVisitados = [listaDeVertices[0]]

    while len(listaDeVisitados) != len(listaDeVertices):
        listaDeVisitados =  fun (G,listaDeVisitados

def fun (G,listaVerticesVisitadas):
    melhorDistancia = float("inf")
    melhorAresta = (-1,1)
    for u in listaDeVisitados:
        for verticeAdjacente in G.edges_iter(u[0]):
            if G[u][verticeAdjacente]["distancia"] < melhorDistancia and G[verticeAdjacente]["visitado"] = False :
                melhorDistancia = G[u][verticeAdjacente]["distancia"]
                melhorAresta = (u,verticeAdjacente)

    if len(listaVerticesVisitadas) == 1:
        G[melhorAresta[0]][melhorAresta[1]]["caminho"] = True
    elif len(listaVerticesVisitadas) == 2:
        G[melhorAresta[0]][melhorAresta[1]]["caminho"] = True
        G[melhorAresta[1]][melhorAresta[listaVerticesVisitadas[1]]]["caminho"] = True
    else:
        novaMelhorDistancia = float("inf")
        for u in listaDeVisitados:
        for verticeAdjacente in G.edges_iter(u[0]):
            if G[u][verticeAdjacente]["distancia"] < melhorDistancia and G[verticeAdjacente]["visitado"] = True and melhorAresta[0] != u :
                novaMelhorDistancia = G[u][verticeAdjacente]["distancia"]
                novaMelhorAresta = (u,verticeAdjacente)

        G[melhorAresta[0]][melhorAresta[1]]["caminho"] = True
        G[melhorAresta[0]][novaMelhorAresta[1]]["caminho"] = False
        G[novaMelhorAresta[0]][novaMelhorAresta[1]]["caminho"] = True
    listaVerticesVisitadas.append(melhorAresta[1])
    return listaVerticesVisitadas
        

        




    

    
        
        
            


            

        






