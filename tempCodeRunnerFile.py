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
    return ((centro.getY() >= centro1.getY()) == (cliente.getY() <= cliente1.getY())) and ((centro.getY() <= centro1.getY()) == (cliente.getY() >= cliente1.getY()))


def distancia(c1, c2):
    return math.sqrt(
        ((c2.getX() - c1.getX()) ** 2) +
        ((c2.getY() - c1.getY()) ** 2))
        
def ler_cliente(x, y, volume, valor, pacotes,flag):
    return Cliente(volume, valor, pacotes, x, y)

def ler_veiculo(V, P, Nv, vf, vd, tc, td, ph, pkm, pf):
    return Veiculo(V, P, Nv, vf, vd, tc, td, ph, pkm, pf) 

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