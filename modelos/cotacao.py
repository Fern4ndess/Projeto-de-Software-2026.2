from datetime import datetime

class Cotacao:

    def __init__(self, moeda_origem, moeda_destino, valor, horario):
        self.__moeda_origem = moeda_origem
        self.__moeda_destino = moeda_destino
        self.__valor = valor
        self.__horario = horario

    @property
    def moeda_origem(self):
        return self.__moeda_origem

    @property
    def moeda_destino(self):
        return self.__moeda_destino

    @property
    def valor(self):
        return self.__valor

    @property
    def horario(self):
        return self.__horario

    def __str__(self):
        return f"{self.__moeda_origem} -> {self.__moeda_destino}: {self.__valor} ({self.__horario})"
