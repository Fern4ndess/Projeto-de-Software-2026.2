from modelos.instrumento import Instrumento

class Criptoativo(Instrumento):

    def __init__(self, codigo):
        super().__init__(codigo)

    def calcular_volatilidade(self):
        return "Volatilidade calculada com base em 24 horas (implementação futura)."

    def __str__(self):
        return f"Criptoativo: {self.codigo}"
