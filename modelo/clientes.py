from math import ceil
class Cliente(object):
    def __init__(self, v, valor, qtdPacotes, coordX, coordY):
        self.volume = v*qtdPacotes*100
        self.__valor = valor
        self.pacotes = qtdPacotes
        self.__coordX = coordX
        self.__coordY = coordY
        self.centro = False

    def getX(self):
        return self.__coordX

    def getY(self):
        return self.__coordY

    def __repr__(self):
        if self.centro:
            return "({0}, {1}, {2}, {3})".format(self.__coordX, self.__coordY, ceil(self.volume), self.pacotes)
        else:    
            return "({0}, {1})".format(self.__coordX, self.__coordY)
