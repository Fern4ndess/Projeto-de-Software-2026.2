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
            valor = input(mensagem).strip()

            # Permite que o usuário digite 10,50
            valor = valor.replace(",", ".")

            numero = Decimal(valor)

            if numero < 0:
                print("O valor não pode ser negativo.")
                continue

            return numero

        except InvalidOperation:
            print(
                "Valor inválido. "
                "Digite um número válido."
            )


def ler_quantidade(mensagem):
    """
    Lê uma quantidade maior que zero.
    """

    while True:

        valor = ler_decimal(mensagem)

        if valor <= Decimal("0"):
            print(
                "A quantidade deve ser maior que zero."
            )
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

        print(
            "O código não pode ficar vazio."
        )


def criar_instrumento():
    """
    Permite escolher entre moeda fiduciária
    e criptoativo.
    """

    print("\n--- TIPO DE INSTRUMENTO ---")
    print("1 - Moeda fiduciária")
    print("2 - Criptoativo")

    while True:

        opcao = input(
            "Escolha: "
        ).strip()

        if opcao == "1":

            codigo = ler_codigo_instrumento()

            return MoedaFiat(codigo)

        elif opcao == "2":

            codigo = ler_codigo_instrumento()

            return Criptoativo(codigo)

        else:

            print(
                "Opção inválida. "
                "Escolha 1 ou 2."
            )


# ==========================================================
# RF1 - COTAÇÕES IMUTÁVEIS
# ==========================================================

def demonstrar_rf1():

    print("\n" + "=" * 60)
    print("RF1 - COTAÇÕES IMUTÁVEIS")
    print("=" * 60)

    codigo_origem = ler_codigo_instrumento()

    moeda_destino = input(
        "Digite a moeda de referência: "
    ).strip().upper()

    valor = ler_quantidade(
        "Digite o valor da cotação: "
    )

    cotacao = Cotacao(
        codigo_origem,
        moeda_destino,
        valor,
        datetime.now()
    )

    print("\nCotação registrada:")

    print(cotacao)

    print(
        "\nA cotação registrada representa "
        "um registro fixo daquele momento."
    )

    print(
        "Uma nova cotação deve ser registrada "
        "como um novo objeto."
    )


# ==========================================================
# RF2 - DINHEIRO
# ==========================================================

def demonstrar_rf2():

    print("\n" + "=" * 60)
    print("RF2 - SEM MISTURA IMPLÍCITA DE MOEDAS")
    print("=" * 60)

    print("\nPrimeiro valor")

    valor1 = ler_decimal(
        "Digite o valor: "
    )

    moeda1 = input(
        "Digite a moeda: "
    ).strip().upper()

    print("\nSegundo valor")

    valor2 = ler_decimal(
        "Digite o valor: "
    )

    moeda2 = input(
        "Digite a moeda: "
    ).strip().upper()

    dinheiro1 = Dinheiro(
        valor1,
        moeda1
    )

    dinheiro2 = Dinheiro(
        valor2,
        moeda2
    )

    try:

        resultado = dinheiro1 + dinheiro2

        print(
            "\nResultado da soma:"
        )

        print(resultado)

    except (ValueError, TypeError) as erro:

        print(
            "\nOperação bloqueada."
        )

        print(
            f"Não é permitido somar "
            f"{moeda1} com {moeda2} "
            f"sem conversão explícita."
        )

        print(
            f"Detalhe: {erro}"
        )


# ==========================================================
# RF3 - HERANÇA
# ==========================================================

def demonstrar_rf3():

    print("\n" + "=" * 60)
    print("RF3 - FAMÍLIAS DE INSTRUMENTOS")
    print("=" * 60)

    print("\n--- MOEDA FIDUCIÁRIA ---")

    codigo_fiat = ler_codigo_instrumento()

    fiat = MoedaFiat(
        codigo_fiat
    )

    print("\n--- CRIPTOATIVO ---")

    codigo_crypto = ler_codigo_instrumento()

    crypto = Criptoativo(
        codigo_crypto
    )

    print("\nInstrumentos criados:")

    print(
        f"Fiat:   {fiat}"
    )

    print(
        f"Crypto: {crypto}"
    )

    print(
        "\nOs dois pertencem à família "
        "Instrumento."
    )


# ==========================================================
# RF4 - EXIBIÇÃO E VOLATILIDADE
# ==========================================================

def demonstrar_rf4():

    print("\n" + "=" * 60)
    print("RF4 - EXIBIÇÃO E VOLATILIDADE")
    print("=" * 60)

    instrumento = criar_instrumento()

    valor = ler_decimal(
        "\nDigite um valor para exibição: "
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
# RF5 - POSIÇÕES DA CARTEIRA
# ==========================================================

def demonstrar_rf5(
    carteira,
    servico
):

    print("\n" + "=" * 60)
    print("RF5 - AVALIAÇÃO MISTA DA CARTEIRA")
    print("=" * 60)

    print(
        "\nAdicionando uma nova posição."
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

    carteira.exibir(
        servico
    )


# ==========================================================
# RF6 - COTAÇÃO MULTIFONTE
# ==========================================================

def demonstrar_rf6(servico):

    print("\n" + "=" * 60)
    print("RF6 - COTAÇÕES MULTIFONTE")
    print("=" * 60)

    instrumento = criar_instrumento()

    try:

        cotacao = servico.obter_cotacao(
            instrumento,
            "BRL"
        )

        print(
            "\nCotação encontrada:"
        )

        print(cotacao)

    except ValueError as erro:

        print(
            "\nNão foi possível obter "
            "a cotação."
        )

        print(
            f"Detalhe: {erro}"
        )


# ==========================================================
# RF7 - CARTEIRA PROTEGIDA
# ==========================================================

def demonstrar_rf7(
    carteira_protegida
):

    while True:

        print("\n" + "=" * 60)
        print("RF7 - CARTEIRA PROTEGIDA")
        print("=" * 60)

        print(
            f"\nSaldo atual: "
            f"R$ {carteira_protegida.saldo:.2f}"
        )

        print("\n1 - Depositar")
        print("2 - Sacar")
        print("3 - Comprar ativo")
        print("4 - Ver posições")
        print("0 - Voltar")

        opcao = input(
            "\nEscolha uma opção: "
        ).strip()

        # --------------------------------------------------
        # DEPÓSITO
        # --------------------------------------------------

        if opcao == "1":

            valor = ler_quantidade(
                "\nDigite o valor do depósito: R$ "
            )

            try:

                carteira_protegida.depositar(
                    valor
                )

                print(
                    "\nDepósito realizado "
                    "com sucesso."
                )

                print(
                    f"Novo saldo: "
                    f"R$ {carteira_protegida.saldo:.2f}"
                )

            except ValueError as erro:

                print(
                    f"\nOperação recusada: "
                    f"{erro}"
                )

        # --------------------------------------------------
        # SAQUE
        # --------------------------------------------------

        elif opcao == "2":

            valor = ler_quantidade(
                "\nDigite o valor do saque: R$ "
            )

            try:

                carteira_protegida.sacar(
                    valor
                )

                print(
                    "\nSaque realizado "
                    "com sucesso."
                )

                print(
                    f"Novo saldo: "
                    f"R$ {carteira_protegida.saldo:.2f}"
                )

            except ValueError as erro:

                print(
                    f"\nOperação recusada: "
                    f"{erro}"
                )

        # --------------------------------------------------
        # COMPRA
        # --------------------------------------------------

        elif opcao == "3":

            print(
                "\n--- COMPRA DE ATIVO ---"
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
                    "\nCompra realizada "
                    "com sucesso."
                )

                print(
                    f"Novo saldo: "
                    f"R$ {carteira_protegida.saldo:.2f}"
                )

            except ValueError as erro:

                print(
                    f"\nCompra recusada: "
                    f"{erro}"
                )

        # --------------------------------------------------
        # POSIÇÕES
        # --------------------------------------------------

        elif opcao == "4":

            carteira_protegida.listar_posicoes()

        # --------------------------------------------------
        # VOLTAR
        # --------------------------------------------------

        elif opcao == "0":

            print(
                "\nVoltando ao menu principal..."
            )

            break

        else:

            print(
                "\nOpção inválida."
            )


# ==========================================================
# CONSULTAR CARTEIRA
# ==========================================================

def consultar_carteira(
    carteira,
    servico
):

    print("\n" + "=" * 60)
    print("CONSULTA DA CARTEIRA")
    print("=" * 60)

    carteira.exibir(
        servico
    )


# ==========================================================
# MENU PRINCIPAL
# ==========================================================

def exibir_menu():

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
    print("7 - RF7 - Carteira protegida")
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
    # CARTEIRA
    # ------------------------------------------------------

    carteira = Carteira()

    # ------------------------------------------------------
    # CARTEIRA PROTEGIDA
    # ------------------------------------------------------

    carteira_protegida = CarteiraProtegida(
        Decimal("5000.00")
    )

    # ------------------------------------------------------
    # MENU PRINCIPAL
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

            print("\n" + "=" * 60)
            print(
                "Encerrando o Painel de Moedas e Economia..."
            )
            print("=" * 60)

            break

        else:

            print(
                "\nOpção inválida."
            )

            print(
                "Digite uma opção entre 0 e 8."
            )


# ==========================================================
# EXECUÇÃO
# ==========================================================

if __name__ == "__main__":
    main()
