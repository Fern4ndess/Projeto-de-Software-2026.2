from decimal import Decimal, InvalidOperation
from datetime import datetime

from modelos.cotacao import Cotacao
from modelos.dinheiro import Dinheiro
from modelos.moeda_fiat import MoedaFiat
from modelos.criptoativo import Criptoativo
from modelos.carteira import Carteira, CarteiraProtegida

from provedores.provedor_fiat import ProvedorFiat
from provedores.provedor_crypto import ProvedorCripto

from servicos.servicos_cotacao import ServicoCotacao


# ==========================================================
# FUNÇÕES AUXILIARES DE ENTRADA
# ==========================================================

def ler_decimal(mensagem):
    """
    Lê um número decimal informado pelo usuário.
    Aceita vírgula ou ponto.
    """

    while True:
        try:
            valor = input(mensagem).strip().replace(",", ".")

            numero = Decimal(valor)

            if numero < 0:
                print("O valor não pode ser negativo.")
                continue

            return numero

        except InvalidOperation:
            print("Valor inválido. Digite um número.")


def ler_quantidade(mensagem):
    """
    Lê uma quantidade maior que zero.
    """

    while True:
        valor = ler_decimal(mensagem)

        if valor <= Decimal("0"):
            print("A quantidade deve ser maior que zero.")
            continue

        return valor


def ler_codigo_instrumento():
    """
    Lê o código do instrumento.
    """

    while True:
        codigo = input(
            "Digite o código do instrumento: "
        ).strip().upper()

        if codigo:
            return codigo

        print("O código não pode ficar vazio.")


def criar_instrumento():
    """
    Permite ao usuário escolher entre moeda fiduciária
    e criptoativo.
    """

    print("\n--- TIPO DE INSTRUMENTO ---")
    print("1 - Moeda fiduciária")
    print("2 - Criptoativo")

    while True:
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            codigo = ler_codigo_instrumento()
            return MoedaFiat(codigo)

        if opcao == "2":
            codigo = ler_codigo_instrumento()
            return Criptoativo(codigo)

        print("Opção inválida.")


# ==========================================================
# RF1
# ==========================================================

def demonstrar_rf1():
    """
    RF1 - Cotações imutáveis.
    """

    print("\n" + "=" * 60)
    print("RF1 - COTAÇÕES IMUTÁVEIS")
    print("=" * 60)

    cotacao = Cotacao(
        "USD",
        "BRL",
        Decimal("5.43"),
        datetime.now()
    )

    print("\nCotação registrada:")
    print(cotacao)

    print(
        "\nA cotação representa um registro daquele momento."
    )

    print(
        "Uma nova cotação deve ser criada como um novo registro."
    )


# ==========================================================
# RF2
# ==========================================================

def demonstrar_rf2():
    """
    RF2 - Não permitir mistura implícita de moedas.
    """

    print("\n" + "=" * 60)
    print("RF2 - SEM MISTURA IMPLÍCITA DE MOEDAS")
    print("=" * 60)

    valor1 = ler_decimal(
        "\nDigite o primeiro valor em BRL: "
    )

    valor2 = ler_decimal(
        "Digite o segundo valor em BRL: "
    )

    dinheiro1 = Dinheiro(
        valor1,
        "BRL"
    )

    dinheiro2 = Dinheiro(
        valor2,
        "BRL"
    )

    print(
        "\nResultado da soma:"
    )

    print(
        dinheiro1 + dinheiro2
    )

    print("\nAgora será testada a mistura de moedas.")

    valor_usd = ler_decimal(
        "Digite um valor em USD: "
    )

    try:

        dinheiro_usd = Dinheiro(
            valor_usd,
            "USD"
        )

        resultado = dinheiro1 + dinheiro_usd

        print(resultado)

    except (ValueError, TypeError) as erro:

        print(
            "\nMistura bloqueada corretamente:"
        )

        print(erro)


# ==========================================================
# RF3
# ==========================================================

def demonstrar_rf3():
    """
    RF3 - Herança entre instrumentos.
    """

    print("\n" + "=" * 60)
    print("RF3 - FAMÍLIAS DE INSTRUMENTOS")
    print("=" * 60)

    print("\n1 - Moeda fiduciária")
    codigo_fiat = ler_codigo_instrumento()

    fiat = MoedaFiat(codigo_fiat)

    print("\n2 - Criptoativo")
    codigo_crypto = ler_codigo_instrumento()

    crypto = Criptoativo(codigo_crypto)

    print("\nInstrumentos cadastrados:")

    print(fiat)
    print(crypto)

    print(
        "\nOs dois pertencem à família Instrumento,"
        " mas possuem comportamentos próprios."
    )


# ==========================================================
# RF4
# ==========================================================

def demonstrar_rf4():
    """
    RF4 - Exibição apropriada ao tipo de instrumento.
    """

    print("\n" + "=" * 60)
    print("RF4 - EXIBIÇÃO E VOLATILIDADE")
    print("=" * 60)

    instrumento = criar_instrumento()

    valor = ler_decimal(
        "\nDigite o valor para exibição: "
    )

    print("\nValor formatado:")

    print(
        instrumento.formatar_valor(valor)
    )

    print("\nCritério de volatilidade:")

    print(
        instrumento.calcular_volatilidade()
    )


# ==========================================================
# RF5
# ==========================================================

def demonstrar_rf5(carteira, servico):
    """
    RF5 - Carteira heterogênea.
    """

    print("\n" + "=" * 60)
    print("RF5 - AVALIAÇÃO MISTA DA CARTEIRA")
    print("=" * 60)

    print(
        "\nVamos adicionar uma posição à carteira."
    )

    instrumento = criar_instrumento()

    quantidade = ler_quantidade(
        "Digite a quantidade: "
    )

    carteira.adicionar_posicao(
        instrumento,
        quantidade
    )

    print(
        "\nPosição adicionada com sucesso."
    )

    carteira.exibir(servico)


# ==========================================================
# RF6
# ==========================================================

def demonstrar_rf6(servico):
    """
    RF6 - Cotações multifonte uniformes.
    """

    print("\n" + "=" * 60)
    print("RF6 - COTAÇÕES MULTIFONTE")
    print("=" * 60)

    instrumento = criar_instrumento()

    try:

        cotacao = servico.obter_cotacao(
            instrumento,
            "BRL"
        )

        print("\nCotação encontrada:")

        print(cotacao)

    except ValueError as erro:

        print(
            "\nNão foi possível obter a cotação:"
        )

        print(erro)


# ==========================================================
# RF7
# ==========================================================

def demonstrar_rf7(carteira_protegida):
    """
    RF7 - Carteira protegida.
    """

    print("\n" + "=" * 60)
    print("RF7 - CARTEIRA PROTEGIDA")
    print("=" * 60)

    print(
        f"\nSaldo atual: "
        f"R$ {carteira_protegida.saldo:.2f}"
    )

    print(
        "\nSerá realizada uma compra."
    )

    instrumento = criar_instrumento()

    quantidade = ler_quantidade(
        "Digite a quantidade comprada: "
    )

    valor = ler_quantidade(
        "Digite o valor total da compra: R$ "
    )

    try:

        carteira_protegida.comprar(
            instrumento,
            quantidade,
            valor
        )

        print(
            "\nCompra realizada com sucesso."
        )

        print(
            f"Novo saldo: "
            f"R$ {carteira_protegida.saldo:.2f}"
        )

        carteira_protegida.listar_posicoes()

    except ValueError as erro:

        print(
            "\nOperação recusada:"
        )

        print(erro)

        print(
            f"Saldo permanece: "
            f"R$ {carteira_protegida.saldo:.2f}"
        )


# ==========================================================
# CONSULTAR CARTEIRA
# ==========================================================

def consultar_carteira(carteira, servico):
    """
    Exibe as posições atuais e o valor total.
    """

    print("\n" + "=" * 60)
    print("CONSULTA DA CARTEIRA")
    print("=" * 60)

    carteira.exibir(servico)


# ==========================================================
# MENU PRINCIPAL
# ==========================================================

def exibir_menu():
    """

    Exibe o menu principal do sistema.
    """

    print("\n")
    print("=" * 60)
    print("       PAINEL DE MOEDAS E ECONOMIA")
    print("=" * 60)

    print("1 - RF1 - Consultar cotação")
    print("2 - RF2 - Trabalhar com dinheiro")
    print("3 - RF3 - Instrumentos")
    print("4 - RF4 - Exibição e volatilidade")
    print("5 - RF5 - Adicionar posição")
    print("6 - RF6 - Consultar cotação multifonte")
    print("7 - RF7 - Comprar ativo")
    print("8 - Consultar carteira")
    print("0 - Sair")

    print("=" * 60)


# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================

def main():

    # ------------------------------------------------------
    # PROVEDORES
    # ------------------------------------------------------

    provedor_fiat = ProvedorFiat()

    provedor_crypto = ProvedorCripto()

    servico = ServicoCotacao(
        [
            provedor_fiat,
            provedor_crypto
        ]
    )

    # ------------------------------------------------------
    # CARTEIRAS
    # ------------------------------------------------------

    carteira = Carteira()

    carteira_protegida = CarteiraProtegida(
        Decimal("5000.00")
    )

    # ------------------------------------------------------
    # MENU
    # ------------------------------------------------------

    while True:

        exibir_menu()

        opcao = input(
            "Digite uma opção: "
        ).strip()

        if opcao == "1":

            demonstrar_rf1()

        elif opcao == "2":

            demonstrar_rf2()

        elif opcao == "3":

            demonstrar_rf3()

        elif opcao == "4":

            demonstrar_rf4()

        elif opcao == "5":

            demonstrar_rf5(
                carteira,
                servico
            )

        elif opcao == "6":

            demonstrar_rf6(
                servico
            )

        elif opcao == "7":

            demonstrar_rf7(
                carteira_protegida
            )

        elif opcao == "8":

            consultar_carteira(
                carteira,
                servico
            )

        elif opcao == "0":

            print("\nEncerrando o sistema...")

            print(
                "Obrigado por utilizar "
                "o Painel de Moedas e Economia."
            )

            break

        else:

            print(
                "\nOpção inválida. "
                "Escolha uma opção do menu."
            )


# ==========================================================
# EXECUÇÃO
# ==========================================================

if __name__ == "__main__":
    main()
