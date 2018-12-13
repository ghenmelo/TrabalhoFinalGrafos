from math import ceil
from math import hypot


class Cliente(object):
    def __init__(self, v, valor, qtdPacotes, coordX, coordY):
        self.volume = v*qtdPacotes*100
        self.__valor = valor
        self.pacotes = qtdPacotes
        self.__coordX = coordX
        self.__coordY = coordY
        self.centro = False

    def getX(self):
        return self.__coordX * 100

    def getY(self):
        return self.__coordY * 100

    def __repr__(self):
        if self.centro:
            return "({0}, {1}, {2}, {3})".format(ceil(self.__coordX), ceil(self.__coordY), ceil(self.volume), self.pacotes)
        else:    
            return "({0}, {1})".format(ceil(self.__coordX), ceil(self.__coordY))
