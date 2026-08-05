class Dinheiro:

    def __init__(self, valor, moeda):
        self.__valor = float(valor)
        self.__moeda = moeda.upper()

    @property
    def valor(self):
        return self.__valor

    @property
    def moeda(self):
        return self.__moeda
