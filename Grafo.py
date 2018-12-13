import networkx as nx
from modelo.veiculo import Veiculo
import random

def TSP (G,veiculo):
    listaDeVertices = []
    for vertice in G.nodes():
        listaDeVertices.append(vertice)

    listaDeVisitados = [listaDeVertices[0]]
    somaVolume = 0
    somaDinheiro = 0
    while len(listaDeVisitados) != len(listaDeVertices) and somaVolume <= veiculo.V and somaDinheiro <= veiculo.P:
        G,listaDeVisitados =  fun (G,listaDeVisitados)
        for i in listaDeVisitados:
            somaDinheiro += G.node[i]["dinheiro"]
            somaVolume += G.node[i]["volume"]
    verticeInicial = listaDeVisitados[0]
    temp = nx.Graph()
    temp = G   
    caminho = {listaDeVisitados[0]}
    for u,v in temp.edges():
        if G[u][v]["caminho"] == True:
            caminho.add(u)
            caminho.add(v)
    for i in caminho:
        if (i != verticeInicial):
            G.remove_node(i)
    if (len(caminho) == 1):
        return temp,caminho
    return G,caminho

def fun (G,listaVerticesVisitadas):
    melhorDistancia = float("inf")
    melhorAresta = (-1,-1)
    for u in listaVerticesVisitadas:
        for x,verticeAdjacente in G.edges(u):
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
            for x,verticeAdjacente in G.edges(u):
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
    melhoresVeiculos = []
    for veiculo in veiculos:
        melhoresVeiculos.append(veiculo)
    melhoresVeiculos.sort(reverse=True, key=lambda veiculo:veiculo.calculaCustoBeneficio())
    i = 0
    while N.size() != 0:
        caminhoAtual = []
        G,caminhoAtual = TSP(G,melhoresVeiculos[0])
        k = 0
        while len(caminhoAtual) == 1 :
            k = 1
            G,caminhoAtual = TSP(G,melhoresVeiculos[k])
            k += 1
            if k == 5:
                raise Exception("Não foi possível resolver")
        print (melhoresVeiculos[k].Nv)
        caminhos.append({i+1:(caminhoAtual,melhoresVeiculos[k].Nv)})
        i += 1
        veiculos[veiculos.index(melhoresVeiculos[k])].Nv -= 1
    print(caminhos)


                
        

    # print ("resultado")
    #     soma = 0
    #     for u,v in G.edges_iter():
    #         if(G[u][v]["caminho"] == True):
    #             soma += G[u][v]["distancia"]
    #             print (u,v)
    #     print (soma)



# Lista de informações sobre os veículos
veiculos = [Veiculo(0, 0, 0, 25, 30, 0.01, 0, 0, 0, 0) for i in range(5)]
# Tipo 0: Van
veiculos[0].V = random.randint(8,16)
veiculos[0].P = random.randint(70000,75000)
veiculos[0].Nv = random.randint(10,20)
veiculos[0].td = random.uniform(0.04, 0.08)
veiculos[0].ph = random.randint(30,60)
veiculos[0].pkm = random.randint(2,4)
veiculos[0].pf = random.randint(100,200)
# Tipo 1: Mini-Van
veiculos[1].V = random.randint(2,4)
veiculos[1].P = random.randint(70000,75000)
veiculos[1].Nv = random.randint(10,20)
veiculos[1].td = random.uniform(0.02, 0.04)
veiculos[1].ph = random.randint(30,60)
veiculos[1].pkm = random.randint(2,4)
veiculos[1].pf = random.randint(90,180)
# Tipo 2: Comum
veiculos[2].V = random.uniform(0.7,1.4)
veiculos[2].P = random.randint(30000,35000)
veiculos[2].Nv = random.randint(20,30)
veiculos[2].td = random.uniform(0.02, 0.04)
veiculos[2].ph = random.randint(30,60)
veiculos[2].pkm = random.randint(1,2)
veiculos[2].pf = random.randint(60,120)
# Tipo 3: Motocicleta
veiculos[3].V = random.uniform(0.02,0.04)
veiculos[3].P = random.randint(1000,5000)
veiculos[3].Nv = random.randint(20,30)
veiculos[3].td = random.uniform(0.02, 0.04)
veiculos[3].ph = random.randint(30,60)
veiculos[3].pkm = random.randint(1,2)
veiculos[3].pf = random.randint(40,80)
# Tipo 4: Van terceirizada
veiculos[4].V = random.uniform(0.08,0.16)
veiculos[4].P = random.randint(75000,80000)
veiculos[4].Nv = 100
veiculos[4].td = random.uniform(0.04, 0.08)
veiculos[4].ph = 0
veiculos[4].pkm = random.randint(2,4)
veiculos[4].pf = 0
# for i in veiculos:
#     print(i.calculaCustoBeneficio())
teste(veiculos)




    

    
        
        
            


            

        






