from src.models.instrumentos import Instrumento

class MoedaFiduciaria(Instrumento):
    def __init__(self, codigo):
        super().__init__(codigo)

    def calcular_volatilidade(self):
        return "Volatilidade calculada sobre 30 dias de cotações diárias."

    def __str__(self):
        return f"Moeda Fiduciária: {self.codigo}"