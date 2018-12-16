import networkx as nx
from modelo.veiculo import Veiculo
import random
#PRECISA COLOCAR A QUESTAO DO TEMPO QUE O VEICULO CIRCULA

#Função que calcula o tempo da trajetória que determinado veículo fez
def CalculaTempo(listaDeVisitados, veiculo, G):
    tempoInicial = veiculo.tc
    tempoDescarga = 0
    for v in listaDeVisitados:
        if v != listaDeVisitados[0]:
           tempoDescarga += G.node[v]["numeroPacotes"]*veiculo.td
    
    tempoLocomocao = 0
    # Faz a soma dos tempos de locomoção
    for u,v in G.edges():
        if(u == listaDeVisitados[0] or v == listaDeVisitados[0])and(G[u][v]["caminho"]==True):
            tempoLocomocao += G[u][v]["distancia"]/veiculo.vf
        
        elif(G[u][v]==True):
            tempoLocomocao += G[u][v]["distancia"]/veiculo.válida

    return (tempoInicial+tempoDescarga+tempoLocomocao)

# TSP é a função avalia se o caminho gerado pela função TSPAux calcula,
# usando em consideração o tempo da trajetória do veículo, o valor em dinheiro que o veículo
# pode carregar e  o volume do trajeto.
def TSP (G,veiculo):
    listaDeVertices = []
    for vertice in G.nodes():
        listaDeVertices.append(vertice)
    listaDeVisitados = [listaDeVertices[0]]
    somaVolume = 0
    somavalor = 0
    somaTempo = 0
    #temporario foi criada com o intuito de salva a ultima trajetória válida que o veiculo pode fazer
    temp = nx.Graph()
    tempLista = []
    #while que verifica se ainda é possivel calcular o um melhor caminho:
    #   Se ainda todas as condições forem satisfeitas, o TSPAux calcula 
    #uma nova trajetória 
    #   Caso o TSPAux retorne um caminho inválido,o G  recebe o valor da ultima itercação.

    while len(listaDeVisitados) != len(listaDeVertices) and somaVolume <= veiculo.V and somavalor <= veiculo.P and somaTempo<=7:
        temp = G.copy()
        tempLista = list(listaDeVisitados)
        G,listaDeVisitados =  TSPaux (G,listaDeVisitados)
        
        for i in listaDeVisitados:
            somavalor += G.node[i]["valor"]
            somaVolume += G.node[i]["volume"]
        if (len(listaDeVisitados) > 1):
            somaTempo = CalculaTempo(listaDeVisitados,veiculo,G)
    if  somaVolume > veiculo.V or somavalor > veiculo.P or somaTempo>7:
        G = temp
        listaDeVisitados = tempLista

    verticeInicial = listaDeVisitados[0]
    #Retorna o caminho atual
    for i in listaDeVisitados:
        if (i != verticeInicial):
            G.remove_node(i)
    return G,listaDeVisitados


# Função que realiza o TSP do vizinho mais proximo
# Ela inicia o ciclo no centro de distribuição e a partir disso enquanto houver casas nao visitadas,
# a função adiciona a casa mais proxima ao ciclio até que todas as casas sejam visitadas

def TSPaux (G,listaVerticesVisitadas):
    melhorDistancia = float("inf")
    melhorAresta = (-1,-1)

    #Acha o novo vertice que irá ser adicionado no ciclo a partir da menor distancia
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


# Função usada para determinar os caminhos por onde um veículo irá passar,ela ordena os veículos a partir de um calculo de custo beneficio,
# a função determina o caminho passando de casa em casa onde o melhor veiculo tem preferencia para fazer a entrega, 
# caso ele não suporte o valor ou o volume a rota é fechada e outro veículo é enviado para a casa, caso nenhum veículo possa realizar a entrega
# não é possível resolver e a função retorna erro
def MontaCaminhos (G,veiculos):
    P = criarGrafo(G)
    # Grafo temporario para que o grafo original não seja alterado
    N = nx.Graph() 
    N = P.copy()
    caminhos = []
    melhoresVeiculos = []
    N.node[1]["volume"] = 0
    N.node[1]["valor"] = 0
    N.node[1]["numeroDePacotes"] = 0

    for veiculo in veiculos:
        melhoresVeiculos.append(veiculo)
    melhoresVeiculos.sort(reverse = True,key=lambda veiculo:veiculo.calculaCustoBeneficio())
    
    iteracao= 0
    
    # Enquanto o grafo tiver vertíces além do centro, é realizado o TSP para a determinação do caminho que o veículo utilizado
    while N.size() != 0:
        k = 0
        for i in range (0,len(melhoresVeiculos)):
            if (melhoresVeiculos[i].Nv > 0):
                k = i
                break
        caminhoAtual = []
        N,caminhoAtual = TSP(N,melhoresVeiculos[0])
        # while utilizado para a mudança de veículo caso o atual não suporte o volume ou o valor da entrega
        while len(caminhoAtual) == 1 :
            k += 1
            if k == 5:
                raise Exception("Não foi possível resolver")
            if melhoresVeiculos[k].Nv > 0:
                N,caminhoAtual = TSP(N,melhoresVeiculos[k])
        caminhos.append({iteracao+1:(caminhoAtual,melhoresVeiculos[k])})
        iteracao += 1
        veiculos[veiculos.index(melhoresVeiculos[k])].Nv -= 1

    # print("Caminho: ", caminhos)
    return voltaOriginal(caminhos,P,G)


#Função usada para que após feito balanceamento, o grafo seja adaptado para realização do TSP
def criarGrafo (C):
    G=nx.Graph()
    cont = 2
    t = 0

    # Cria os vertíces do grafo adaptado
    for i in C.nodes():
        if(i.centro == True):
            
            G.add_node(1,volume=i.volume,valor=i.getValor(),numeroPacotes=i.pacotes,coordX=i.getX(),coordY=i.getY(),centro=i.centro,visitado = False)
        
        else:
            G.add_node(cont,volume=i.volume,valor=i.getValor(),numeroPacotes=i.pacotes,coordX=i.getX(),coordY=i.getY(),centro=i.centro,visitado = False)
            cont += 1

    # print ("numero de vertices :",len(list(G.nodes())))

    # Cria as arestas do grafo adaptado, comparando se o [i][j] == [u][v] respectivamente 
    # onde [i][j] são os indices dos vertices e [u][v] são os clientes
    for i in range(1,1+len(list(G.nodes()))):
        for j in range(i+1,1+len(list(G.nodes()))): 
            for u,v in C.edges():
                w = u.getValor()
                x = u.getX()
                y = u.getY()
                w1 = v.getValor()
                x1 = v.getX()
                y1 = v.getY()
                if  u.volume == G.node[i]["volume"] and w == G.node[i]["valor"] and u.pacotes == G.node[i]["numeroPacotes"] and x == G.node[i]["coordX"] and y == G.node[i]["coordY"] and u.centro == G.node[i]["centro"]:
                    if  v.volume == G.node[j]["volume"] and w1 == G.node[j]["valor"] and v.pacotes == G.node[j]["numeroPacotes"] and x1 == G.node[j]["coordX"] and y1 == G.node[j]["coordY"] and v.centro == G.node[j]["centro"]:
                        G.add_edges_from([(i,j)],distancia = C[u][v]["distancia"],caminho = False)
    # print("Vértices: ", len(list(G.nodes())))
    # print("Arestas: ", len(list(G.edges())))
    return G

def voltaOriginal(caminho, G, grafoOriginal):
    listaCaminho = []
    listaTeste = []
    for k in range (len(caminho)):
        listaCaminho.append({k+1:([],caminho[k][k+1][1])})
        for i in caminho[k][k+1][0]:
            for j in grafoOriginal.nodes():
                if  j.volume == G.node[i]["volume"] and j.getValor() == G.node[i]["valor"] and j.pacotes == G.node[i]["numeroPacotes"] and j.getX() == G.node[i]["coordX"] and j.getY() == G.node[i]["coordY"] and j.centro == G.node[i]["centro"]:
                    listaCaminho[k][k+1][0].append(j)
    return listaCaminho
    




    

    
        
        
            


            

        






