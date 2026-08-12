from datetime import datetime
from decimal import Decimal

from modelos.cotacao import Cotacao
from modelos.dinheiro import Dinheiro
from modelos.moeda_fiat import MoedaFiat
from modelos.criptoativo import Criptoativo
from modelos.carteira import (
    Carteira,
    CarteiraProtegida
)

from provedores.provedor_fiat import (
    ProvedorFiat
)

from provedores.provedor_crypto import (
    ProvedorCripto
)

from servicos.servicos_cotacao import (
    ServicoCotacao
)


def main():

    print("=" * 65)
    print(
        "PAINEL DE MOEDAS E ECONOMIA"
    )
    print("=" * 65)

    # --------------------------------------------------
    # RF1 - COTAÇÃO IMUTÁVEL
    # --------------------------------------------------

    print("\nRF1 - COTAÇÃO")

    cotacao = Cotacao(
        "USD",
        "BRL",
        Decimal("5.43"),
        datetime.now()
    )

    print(cotacao)

    # --------------------------------------------------
    # RF2 - SEM MISTURA DE MOEDAS
    # --------------------------------------------------

    print("\nRF2 - DINHEIRO")

    dinheiro1 = Dinheiro(
        Decimal("100"),
        "BRL"
    )

    dinheiro2 = Dinheiro(
        Decimal("50"),
        "BRL"
    )

    print(
        "Soma:",
        dinheiro1 + dinheiro2
    )

    try:

        dinheiro1 + Dinheiro(
            Decimal("50"),
            "USD"
        )

    except ValueError as erro:

        print(
            "Mistura bloqueada:",
            erro
        )

    # --------------------------------------------------
    # RF3 - HERANÇA
    # --------------------------------------------------

    print("\nRF3 - INSTRUMENTOS")

    fiat = MoedaFiat("USD")
    cripto = Criptoativo("BTC")

    print(fiat)
    print(cripto)

    # --------------------------------------------------
    # RF4 - FORMATAÇÃO E VOLATILIDADE
    # --------------------------------------------------

    print("\nRF4 - EXIBIÇÃO")

    print(
        "Fiat:",
        fiat.formatar_valor(
            Decimal("1234.50")
        )
    )

    print(
        "Cripto:",
        cripto.formatar_valor(
            Decimal("0.12345678")
        )
    )

    print(
        "Fiat:",
        fiat.calcular_volatilidade()
    )

    print(
        "Cripto:",
        cripto.calcular_volatilidade()
    )

    # --------------------------------------------------
    # RF6 - PROVEDORES
    # --------------------------------------------------

    print("\nRF6 - PROVEDORES")

    provedor_fiat = ProvedorFiat()
    provedor_cripto = ProvedorCripto()

    servico = ServicoCotacao(
        [
            provedor_fiat,
            provedor_cripto
        ]
    )

    cotacao_usd = servico.obter_cotacao(
        fiat,
        "BRL"
    )

    cotacao_btc = servico.obter_cotacao(
        cripto,
        "BRL"
    )

    print(
        "USD:",
        cotacao_usd
    )

    print(
        "BTC:",
        cotacao_btc
    )

    # --------------------------------------------------
    # RF5 - CARTEIRA
    # --------------------------------------------------

    print("\nRF5 - CARTEIRA")

    carteira = Carteira()

    carteira.adicionar_posicao(
        fiat,
        Decimal("100")
    )

    carteira.adicionar_posicao(
        cripto,
        Decimal("0.01")
    )

    carteira.exibir(servico)

    # --------------------------------------------------
    # RF7 - CARTEIRA PROTEGIDA
    # --------------------------------------------------

    print("\nRF7 - CARTEIRA PROTEGIDA")

    carteira_protegida = CarteiraProtegida(
        Decimal("5000")
    )

    print(
        f"Saldo inicial: "
        f"R$ {carteira_protegida.saldo:.2f}"
    )

    carteira_protegida.comprar(
        fiat,
        Decimal("100"),
        Decimal("1000")
    )

    print(
        f"Saldo após compra: "
        f"R$ {carteira_protegida.saldo:.2f}"
    )

    try:

        carteira_protegida.comprar(
            cripto,
            Decimal("1"),
            Decimal("10000")
        )

    except ValueError as erro:

        print(
            "Compra bloqueada:",
            erro
        )

    print("\n" + "=" * 65)
    print("TESTE DOS RF1-RF7 CONCLUÍDO")
    print("=" * 65)


if __name__ == "__main__":
    main()
