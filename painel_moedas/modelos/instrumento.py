from abc import ABC, abstractmethod

class Instrumento(ABC):
    """
    RF3 [A/H]
    Classe abstrata para qualquer instrumento financeiro.
    """

    def __init__(self, codigo):
        self._codigo = codigo

    @property
    def codigo(self):
        return self._codigo

    @abstractmethod
    def calcular_volatilidade(self):
        pass
