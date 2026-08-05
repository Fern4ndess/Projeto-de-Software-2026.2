from modelos.instrumento import Instrumento

class MoedaFiat(Instrumento):

    def __init__(self, codigo):
        super().__init__(codigo)

    def calcular_volatilidade(self):
        return "Volatilidade calculada com base em 30 dias (implementação futura)."

    def __str__(self):
        return f"Moeda Fiat: {self.codigo}"
