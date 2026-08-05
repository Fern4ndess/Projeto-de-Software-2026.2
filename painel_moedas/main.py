from datetime import datetime

from modelos.cotacao import Cotacao
from modelos.dinheiro import Dinheiro
from modelos.moeda_fiat import MoedaFiat
from modelos.criptoativo import Criptoativo


def main():
    # RF1
    cotacao = Cotacao("USD", "BRL", 5.43, datetime.now())
    print(cotacao)

    # RF2
    dinheiro1 = Dinheiro(100, "BRL")
    dinheiro2 = Dinheiro(50, "BRL")
    print(dinheiro1 + dinheiro2)

    # RF3
    fiat = MoedaFiat("BRL")
    cripto = Criptoativo("BTC")

    print(fiat.calcular_volatilidade())
    print(cripto.calcular_volatilidade())


if __name__ == "__main__":
    main()
