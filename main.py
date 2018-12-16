# -*- coding: utf-8 -*-
import networkx as nx
import math 
import random
import matplotlib.pyplot as a
import matplotlib as mpl
import copy
from Grafo import MontaCaminhos

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

nome_arquivo = input("Informe o arquivo de entrada: ")

arquivo = open("docs/{0}".format(nome_arquivo), "r")

qtd_casas = int(arquivo.readline())
qtd_centros = int(arquivo.readline())
qtd_veiculos = int(arquivo.readline())
qtd_horas = int(arquivo.readline())

# para cada centro de distribuição, existe um grafo
regioes = {}

clientes = []
veiculos = []

for i in range(qtd_centros):
    leitura = arquivo.readline().split()
    cliente = ler_cliente(float(leitura[0]), float(leitura[1]), float(leitura[2]), float(leitura[3]), float(leitura[4]), True)
    cliente.centro = True
    cliente.maior_distancia = 0 - float("inf")

    regioes[cliente] = nx.Graph()
    regioes[cliente].add_node(cliente, pos = (cliente.getX(), cliente.getY()))

for i in range(qtd_casas - qtd_centros):
    leitura = arquivo.readline().split()
    clientes.append(ler_cliente(float(leitura[0]), float(leitura[1]), float(leitura[2]), float(leitura[3]), float(leitura[4]), False))

for i in range(qtd_veiculos):
    leitura = arquivo.readline().split()    
    veiculos.append(ler_veiculo(float(leitura[0]), float(leitura[1]), float(leitura[2]), float(leitura[3]),
    float(leitura[4]), float(leitura[5]), float(leitura[6]), float(leitura[7]), float(leitura[8]), float(leitura[9])))

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
    regioes[menor_centro].add_edge(cliente, menor_centro, distancia=menor_distancia)
    menor_centro.volume += cliente.volume
    menor_centro.pacotes += cliente.pacotes

    # encontra a maior distancia de cliente e centro
    if menor_centro.maior_distancia < menor_distancia:
        menor_centro.maior_distancia = menor_distancia

    volume_total += cliente.volume

for i in regioes.keys():
    grafo = regioes[i]
    print("Quantidade de vizinhos: ", len(list(grafo.neighbors(i))))
for i in regioes.keys():
    print("Volume: ", i.volume)

centros = list(regioes.keys())

completo = nx.union(regioes[centros[0]], regioes[centros[1]])
completo = nx.union(completo, regioes[centros[2]])
completo = nx.union(completo, regioes[centros[3]])
completo = nx.union(completo, regioes[centros[4]])

mapeamento_x = []
mapeamento_y = []

for cliente in completo.nodes():
    if cliente not in centros:
        mapeamento_x.append(cliente.getX())
        mapeamento_y.append(cliente.getY())

mpl.rc("axes", edgecolor="blue")
a.plot(mapeamento_x, mapeamento_y, "ro")

mapeamento_x = []
mapeamento_y = []

for centro in centros:
    mapeamento_x.append(centro.getX())
    mapeamento_y.append(centro.getY())

a.plot(mapeamento_x, mapeamento_y, "bo")

mapeamento_x = []
mapeamento_y = []

for centro in centros:
    for u, v in regioes[centro].edges():
        a.plot([u.getX(), v.getX()], [u.getY(), v.getY()], "--k")
a.axis([0, 100, 0, 100])
a.show()

color_map = ["blue" if vertice in regioes.keys() else "red" for vertice in completo.nodes()]

nx.draw_spring(completo, node_color = color_map)

a.savefig("completo.png")

# transforma em grafo completo
for centro in regioes.keys():
    # pega os clientes do centro
    grafo = regioes[centro]
    clientes_adjacentes = list(grafo.nodes())

    for u in clientes_adjacentes:
        for v in clientes_adjacentes:
            if not grafo.has_edge(u, v) and not grafo.has_edge(v, u) and u is not v:
                grafo.add_edge(u, v, distancia=distancia(u, v))



# grafos completos estão dentro de regioes {}
# lista de veículos estão dentro de veículos[]
veiculos_melhorados = {}

print("Veiculos: ", veiculos)

for centro in regioes.keys():
    volume_temp = centro.volume / volume_total

    veiculos_temp = [copy.copy(x) for x in veiculos]

    for veiculo in veiculos_temp:
        veiculo.Nv = math.floor(veiculo.Nv * volume_temp)

    veiculos_melhorados[centro] = veiculos_temp


regiao = list(regioes.keys())[0]
MontaCaminhos(regioes[regiao],veiculos_melhorados[regiao])

# em veículos melhorados, tem uma lista de carros proporcional
# para cada veículo. Se quiser os veiculos para o centro Z, então
# basta fazer veiculos_melhorados[Z] 

# só usar