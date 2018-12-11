import networkx as nx
import math 
import random
import matplotlib.pyplot as a

from modelo.clientes import Cliente

def distancia(c1, c2):
    return math.sqrt(
        ((c2.getX() - c1.getX()) ** 2) +
        ((c2.getY() - c1.getY()) ** 2))

def ler_cliente(x, y, flag):
    # x, y = float(input("Digite a coordenada X: ")), float(input("Digite a coordenada Y: "))
    # valor = float(input("Informe o valor do pedido: "))
    valor = random.uniform(0, 50) if not flag else 0
    # volume = float(input("Informe o volume dos pacotes: "))
    volume = random.uniform(0, 25) if not flag else 0
    # pacotes = int(input("Informe a quantidade de pacotes: "))
    pacotes = random.randint(0, 10) if not flag else 0
    return Cliente(volume, valor, pacotes, x, y)

qtd_casas = int(input("Digite a quantidade de casas: "))
qtd_centros = int(input("Informe a quantidade de centros de distribuições: "))

# para cada centro de distribuição, existe um grafo
regioes = {}

clientes = []

arquivo = open("entradas.txt", "+r")

for i in range(qtd_centros):
    leitura = arquivo.readline().split()
    cliente = ler_cliente(int(leitura[0]), int(leitura[1]), True)
    cliente.centro = True

    regioes[cliente] = nx.Graph()
    regioes[cliente].add_node(cliente)

for i in range(qtd_casas - qtd_centros):
    leitura = arquivo.readline().split()
    clientes.append(ler_cliente(int(leitura[0]), int(leitura[1]), False))


# primeira classificação - considerando as distancias entre 
# pontos 
for cliente in clientes: 
    menorCentro = list(regioes.keys())[0]
    menorDistancia = distancia(cliente, menorCentro)

    for centro in regioes.keys():
        if (distancia(cliente, centro) < distancia(cliente, menorCentro)):
            menorCentro = centro
            menorDistancia = distancia(cliente, centro)

    regioes[menorCentro].add_node(cliente)
    regioes[menorCentro].add_edge(cliente, menorCentro, weight=menorDistancia)
    menorCentro.volume += cliente.volume
    menorCentro.pacotes += cliente.pacotes


# centro = list(regioes.keys())[2]
# grafo = regioes[centro]
# nx.draw(grafo, with_labels=True)
# a.savefig("graph{0}.png".format(i))
i = 0
for centro in regioes.keys():
    grafo = regioes[centro]

    pos = nx.spring_layout(grafo)
    color_map = ["blue" if vertice in regioes.keys() else "red" for vertice in grafo.nodes()]

    nx.draw(grafo, node_color = color_map, with_labels=True)
    a.savefig("graph{0}.png".format(i))

    a.clf()

    i = i +1
    for u, v in grafo.adjacency():
        v = list(v.keys())[0]
        print("({0},{1})-({2},{3})".format(u.getX(), u.getY(), v.getX(), v.getY()))



# segunda classificação - considerando o volume presente na
# demanda do centro 




# terceira classificação - considerando a quantidade de entregas
# combinado com o preço 
