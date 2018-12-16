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

def intersecao(centro, cliente, centro1, cliente1):
    det = (cliente1.getX() - centro1.getX()) * (cliente.getY() - centro.getY())  -  (cliente1.getY() - centro1.getY()) * (cliente.getX() - centro.getX())
    return det != 0

def existe_intersecao(centro, cliente, centro1, cliente1):
    # print("({0},{1}), ({2},{3}), ({4},{5}), ({6},{7})".format(centro.getX(), centro.getY(), cliente.getX(), cliente.getY(), centro1.getX(), centro1.getY(), cliente1.getX(), cliente1.getY()))
    return ((centro.getY() >= centro1.getY()) == (cliente.getY() <= cliente1.getY())) and ((centro.getY() <= centro1.getY()) == (cliente.getY() >= cliente1.getY()))


def distancia(c1, c2):
    return math.sqrt(
        ((c2.getX() - c1.getX()) ** 2) +
        ((c2.getY() - c1.getY()) ** 2))
        
def ler_cliente(x, y, volume, valor, pacotes,flag):
    return Cliente(volume, valor, pacotes, x, y)

def ler_veiculo(V, P, Nv, vf, vd, tc, td, ph, pkm, pf):
    return Veiculo(V, P, Nv, vf, vd, tc, td, ph, pkm, pf)

def imprime_grafo_simples(grafo, nome_arquivo, limite):
    centros = [x for x in grafo.nodes() if x.centro is True]
    
    mpl.rc("axes", edgecolor="blue")
    a.plot([x.getX() for x in centros], [x.getY() for x in centros], "bo")

    mapeamento_x = []
    mapeamento_y = []

    for vertice in grafo.nodes():
        if vertice not in centros:
            mapeamento_x.append(cliente.getX())
            mapeamento_y.append(cliente.getY())

    a.plot(mapeamento_x, mapeamento_y, "ro")

    for (u, v) in grafo.edges():
        a.plot([u.getX(), v.getX()], [u.getY(), v.getY()], "--k")

    a.axis([0, limite, 0, limite])
    
    a.savefig(nome_arquivo)

def imprime_grafo(regioes, nome_arquivo, limite):
    a.clf()
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
    a.axis([0, limite, 0, limite])

    a.savefig(nome_arquivo)

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
distancia_total = 0

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
    
    menor_centro.soma_distancias += distancia(cliente, menor_centro)

    # encontra a maior distancia de cliente e centro
    if menor_centro.maior_distancia < menor_distancia:
        menor_centro.maior_distancia = menor_distancia

    volume_total += cliente.volume

imprime_grafo(regioes, "exibicao/{0}sem-melhoria.png".format(nome_arquivo), qtd_casas)

centros = list(regioes.keys())
demanda_ideal = (qtd_casas - qtd_centros) / qtd_centros

for centro in regioes.keys():
    grafo = regioes[centro]
    
    if (len(list(grafo.neighbors(centro))) <= demanda_ideal):
        continue
    
    for cliente in list(grafo.neighbors(centro)):
        centros.sort(reverse=True, key=lambda centro : distancia(centro, cliente))
        
        if (len(list(regioes[centros[1]].neighbors(centros[1]))) < demanda_ideal):
            if (centros[1].maior_distancia * 1.2) >= distancia(cliente, centros[1]):
                grafo.remove_node(cliente)
                regioes[centros[1]].add_node(cliente)
                regioes[centros[1]].add_edge(cliente, centros[1], distancia=distancia(centros[1], cliente))
        elif (len(list(regioes[centros[2]].neighbors(centros[2]))) <= demanda_ideal):
            if (centros[2].maior_distancia * 1.2) >= distancia(cliente, centros[2]):
                grafo.remove_node(cliente)
                regioes[centros[2]].add_node(cliente)
                regioes[centros[2]].add_edge(cliente, centros[2], distancia=distancia(centros[2], cliente))
        
        if (len(list(grafo.neighbors(centro))) <= demanda_ideal):
            break

imprime_grafo(regioes, "exibicao/{0}com-melhoria.png".format(nome_arquivo), qtd_casas)

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

for centro in regioes.keys():
    volume_temp = centro.volume / volume_total

    veiculos_temp = [copy.copy(x) for x in veiculos]

    for veiculo in veiculos_temp:
        veiculo.Nv = math.floor(veiculo.Nv * volume_temp)

    veiculos_melhorados[centro] = veiculos_temp

grafo = nx.Graph()

# centros = list(regioes.keys())

# MontaCaminhos(regioes[centros[0]], veiculos_melhorados[centros[0]])
# MontaCaminhos(regioes[centros[1]], veiculos_melhorados[centros[1]])
# MontaCaminhos(regioes[centros[2]], veiculos_melhorados[centros[2]])
# MontaCaminhos(regioes[centros[1]], veiculos_melhorados[centros[1]])
# MontaCaminhos(regioes[centros[4]], veiculos_melhorados[centros[4]])

total = 0

for regiao in regioes.keys():
    grafo.add_nodes_from(list(regioes[regiao].nodes()))

    resultado = MontaCaminhos(regioes[regiao],veiculos_melhorados[regiao])

    for caminho in resultado:
        
        km_percorrido = 0
        tempo_percorrido = 0
        veiculo_utilizado = None

        for rota_temp in caminho.keys():
            rota, veiculo = caminho[rota_temp]
            
            veiculo_utilizado = veiculo
            
            for i in range(len(rota)-1):
                if i == 0:
                    # contar o tempo gasto no descarregamento do centro ao primeiro cliente
                    tempo_percorrido += veiculo.tc
                else:
                    # contar o tempo gasto no descarregamento de cliente para cliente
                    tempo_percorrido += veiculo.td
                
                km_percorrido += distancia(rota[i], rota[i+1])
                grafo.add_edge(rota[i], rota[i+1], distancia=distancia(rota[i], rota[i+1]))


        # contar o tempo gasto no descarregamento de um cliente e volta para centro
        tempo_percorrido += veiculo_utilizado.tc
        km_percorrido += distancia(rota[0],rota[len(rota)-1])

        tempo_percorrido += km_percorrido / veiculo_utilizado.vd

        grafo.add_edge(rota[0], rota[len(rota)-1])

        custo_por_km = km_percorrido * veiculo_utilizado.pkm
        custo_por_hr = tempo_percorrido * veiculo_utilizado.ph
        custo_fixo = veiculo_utilizado.pf

        total_veiculo = custo_fixo + custo_por_hr + custo_por_km   
        print("Tempo gasto: ", tempo_percorrido)
        print("Rota com veículo ", veiculo_utilizado, " gastou: ", total_veiculo)

        total += total_veiculo
    
print("Total de gastos: ", total)

imprime_grafo_simples(grafo, "exibicao/rotas", qtd_casas)