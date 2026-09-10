from decimal import Decimal

from modelos.instrumento import Instrumento


class MoedaFiat(Instrumento):

    def calcular_volatilidade(self):
        return (
            "Critério: cotações diárias "
            "em uma janela de 30 dias."
        )

    def formatar_valor(self, valor):
    valor = Decimal(str(valor))

    return f"R$ {valor:.2f}".replace(".", ",")

    def __str__(self):
        return (
            f"{self.codigo} - Moeda fiduciária"
        )
