# -*- coding: utf-8 -*-
import networkx as nx
import math 
import random
import matplotlib.pyplot as a

from modelo.clientes import Cliente
from modelo.veiculo import Veiculo

def distancia(c1, c2):
    return math.sqrt(
        ((c2.getX() - c1.getX()) ** 2) +
        ((c2.getY() - c1.getY()) ** 2))
        
def ler_cliente(x, y, volume, valor, pacotes,flag):
    # x, y = float(input("Digite a coordenada X: ")), float(input("Digite a coordenada Y: "))
    #valor = float(input("Informe o valor do pedido: "))
    #valor = random.uniform(0, 50) if not flag else 0
    #volume = float(input("Informe o volume dos pacotes: "))
    #volume = random.uniform(0, 25) if not flag else 0
    #pacotes = int(input("Informe a quantidade de pacotes: "))
    #pacotes = random.randint(0, 10) if not flag else 0
    return Cliente(volume, valor, pacotes, x, y)

def ler_veiculo(V, P, Nv, vf, vd, tc, td, ph, pkm, pf):
    return Veiculo(V, P, Nv, vf, vd, tc, td, ph, pkm, pf)  

qtd_casas = int(input("Digite a quantidade de casas: "))
qtd_centros = int(input("Informe a quantidade de centros de distribuições: "))
qtd_veiculos = int(input("Informe a quantidade diferente de veículos disponíveis: "))
qtd_horas = int (input("Digite o número de horas da jornada diária: "))

# para cada centro de distribuição, existe um grafo
regioes = {}

clientes = []
veiculo = []

arquivo = open("docs/InstanciaTeste.txt", "+r")

for i in range(qtd_centros):
    leitura = arquivo.readline().split()
    cliente = ler_cliente(float(leitura[0]), float(leitura[1]), float(leitura[2]), float(leitura[3]), float(leitura[4]), True)
    cliente.centro = True

    regioes[cliente] = nx.Graph()
    regioes[cliente].add_node(cliente, pos = (cliente.getX(), cliente.getY()))

for i in range(qtd_casas - qtd_centros):
    leitura = arquivo.readline().split()
    clientes.append(ler_cliente(float(leitura[0]), float(leitura[1]), float(leitura[2]), float(leitura[3]), float(leitura[4]), False))

for i in range(qtd_veiculos):
    leitura = arquivo.readline().split()    
    veiculo.append(ler_veiculo(float(leitura[0]), float(leitura[1]), float(leitura[2]), float(leitura[3]),
    float(leitura[4]), float(leitura[5]), float(leitura[6]), float(leitura[7]), float(leitura[8]), float(leitura[9])))

print("a")

volume_total = 0

# definição a partir de proximidade
for cliente in clientes: 
    menor_centro = list(regioes.keys())[0]
    menor_distancia = distancia(cliente, menor_centro)
    
    for centro in regioes.keys():
        if (distancia(cliente, centro) < distancia(cliente, menor_centro)):
            menor_centro = centro
            menor_distancia = distancia(cliente, centro)

    regioes[menor_centro].add_node(cliente)
    regioes[menor_centro].add_edge(cliente, menor_centro, weight=menor_distancia, pos = (cliente.getX(), cliente.getY()))
    menor_centro.volume += cliente.volume
    menor_centro.pacotes += cliente.pacotes

    volume_total += cliente.volume

print("b")

# segunda classificação - considerando o volume presente na
# demanda do centro   
volume_ideal = volume_total / qtd_centros

for centro in regioes.keys():
    if (centro.volume <= volume_ideal):
        continue
    
    print("Balanceando centro com volume: ", centro.volume)

    # ordena a partir dos clientes mais distantes
    clientes = list(regioes[centro].neighbors(centro))
    clientes.sort(reverse=True, key=lambda cliente : distancia(centro, cliente))
    # quantidade de clientes que serão deslocados, garantidos pela taxa de 87%
    # de melhoria das distribuições de serviços
    qtd_melhoria = math.floor(len(clientes) * 0.90)
    while qtd_melhoria > 0 and centro.volume > volume_ideal:
        # pega o cliente
        cliente = clientes.pop(0)
        # remove esse cliente para entrega deste centro de distribuição
        regioes[centro].remove_node(cliente)
        
        # atualiza o volume
        centro.volume -= cliente.volume

        possiveis_centros = list(regioes.keys())
        possiveis_centros.remove(centro)

        possiveis_centros.sort(reverse=True, key=lambda c: distancia(c, cliente))
        
        definiu = False

        while not definiu and len(possiveis_centros) > 0:
            possivel_centro = possiveis_centros.pop(0)

            if (possivel_centro.volume + cliente.volume) <= volume_ideal:

                definiu = True
                regioes[possivel_centro].add_node(cliente)
                regioes[possivel_centro].add_edge(cliente, possivel_centro, weight=distancia(possivel_centro, cliente))
                possivel_centro.volume += cliente.volume

        # caso não seja encontrado um outro centro de distribuição que 
        # consiga atender este cliente, ele deverá ainda ser atendido pelo
        # centro em que já se encontrava
        if not definiu:
            regioes[centro].add_node(cliente)
            regioes[centro].add_edge(cliente, centro, weight=distancia(centro, cliente))
            centro.volume += cliente.volume

        # atualiza a quantidade de clientes que podem ser melhorados
        qtd_melhoria -= 1
    
    print("Centro balanceado. Novo volume: ", centro.volume)
    print()
print("Volume ideal: ", volume_ideal)

# primeira classificação - considerando as distancias entre 
# pontos
centros = list(regioes.keys())
demanda_ideal = (qtd_casas - qtd_centros) / qtd_centros

for centro in regioes.keys():
    grafo = regioes[centro]
    
    if (len(list(grafo.neighbors(centro))) <= demanda_ideal):
        continue
    
    for cliente in list(grafo.neighbors(centro)):
        centros.sort(reverse=True, key=lambda centro : distancia(centro, cliente))
        
        if (len(list(regioes[centros[1]].neighbors(centros[1]))) < demanda_ideal):
            grafo.remove_node(cliente)
            regioes[centros[1]].add_node(cliente)
            regioes[centros[1]].add_edge(cliente, centros[1], weight=distancia(centros[1], cliente))
        elif (len(list(regioes[centros[2]].neighbors(centros[2]))) <= demanda_ideal):
            grafo.remove_node(cliente)
            regioes[centros[2]].add_node(cliente)
            regioes[centros[2]].add_edge(cliente, centros[2], weight=distancia(centros[2], cliente))
        
        if (len(list(grafo.neighbors(centro))) <= demanda_ideal):
            break



for i in regioes.keys():
    grafo = regioes[i]
    print("Quantidade de vizinhos: ", len(list(grafo.neighbors(i))))
for i in regioes.keys():
    print("Volume: ", i.volume)


i = 0
for centro in regioes.keys():
    grafo = regioes[centro]

    pos = nx.spring_layout(grafo)
    color_map = ["blue" if vertice in regioes.keys() else "red" for vertice in grafo.nodes()]

    nx.draw(grafo, node_color = color_map, with_labels=True)
    a.savefig("exibicao/graph{0}.png".format(i))

    a.clf()

    i = i + 1

# terceira classificação - considerando a quantidade de entregas
# combinado com o preço 
