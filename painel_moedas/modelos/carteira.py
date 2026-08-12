from decimal import Decimal

from modelos.posicao import Posicao


class Carteira:

    def __init__(self):
        self.__posicoes = []

    def adicionar_posicao(self, instrumento, quantidade):

        posicao = Posicao(
            instrumento,
            quantidade
        )

        self.__posicoes.append(posicao)

    def obter_posicoes(self):

        return tuple(self.__posicoes)

    def calcular_total(self, servico):

        total = Decimal("0")

        for posicao in self.__posicoes:

            total += posicao.valor_em_reais(
                servico
            )

        return total

    def exibir(self, servico):

        if not self.__posicoes:
            print("\nCarteira vazia.")
            return

        print("\n" + "-" * 65)
        print("POSIÇÕES DA CARTEIRA")
        print("-" * 65)

        for posicao in self.__posicoes:

            valor = posicao.valor_em_reais(
                servico
            )

            print(
                f"{posicao.instrumento.codigo:<6} | "
                f"Quantidade: "
                f"{posicao.quantidade:<12} | "
                f"Valor em BRL: "
                f"R$ {valor:,.2f}"
            )

        print("-" * 65)

        total = self.calcular_total(servico)

        print(
            f"TOTAL DA CARTEIRA: "
            f"R$ {total:,.2f}"
        )


# ==========================================================
# RF7 - CARTEIRA PROTEGIDA
# ==========================================================

class CarteiraProtegida:

    def __init__(self, saldo_inicial):

        saldo_inicial = Decimal(
            str(saldo_inicial)
        )

        if saldo_inicial < Decimal("0"):
            raise ValueError(
                "O saldo não pode ser negativo."
            )

        self.__saldo = saldo_inicial
        self.__posicoes = []

    # ------------------------------------------------------
    # CONSULTA DO SALDO
    # ------------------------------------------------------

    @property
    def saldo(self):
        return self.__saldo

    # ------------------------------------------------------
    # ENTRADA DE DINHEIRO
    # ------------------------------------------------------

    def depositar(self, valor):

        valor = Decimal(
            str(valor)
        )

        if valor <= Decimal("0"):
            raise ValueError(
                "O valor do depósito deve ser "
                "maior que zero."
            )

        self.__saldo += valor

    # ------------------------------------------------------
    # SAÍDA DE DINHEIRO
    # ------------------------------------------------------

    def sacar(self, valor):

        valor = Decimal(
            str(valor)
        )

        if valor <= Decimal("0"):
            raise ValueError(
                "O valor do saque deve ser "
                "maior que zero."
            )

        if valor > self.__saldo:
            raise ValueError(
                "Saldo insuficiente para realizar "
                "o saque."
            )

        self.__saldo -= valor

    # ------------------------------------------------------
    # COMPRA DE ATIVO
    # ------------------------------------------------------

    def comprar(
        self,
        instrumento,
        quantidade,
        valor_total
    ):

        quantidade = Decimal(
            str(quantidade)
        )

        valor_total = Decimal(
            str(valor_total)
        )

        if quantidade <= Decimal("0"):
            raise ValueError(
                "A quantidade deve ser "
                "maior que zero."
            )

        if valor_total <= Decimal("0"):
            raise ValueError(
                "O valor da operação deve ser "
                "maior que zero."
            )

        if valor_total > self.__saldo:
            raise ValueError(
                "Saldo insuficiente para realizar "
                "a compra."
            )

        self.__saldo -= valor_total

        self.__posicoes.append(
            Posicao(
                instrumento,
                quantidade
            )
        )

    # ------------------------------------------------------
    # LISTAGEM DAS POSIÇÕES
    # ------------------------------------------------------

    def listar_posicoes(self):

        if not self.__posicoes:

            print(
                "\nNenhuma posição cadastrada."
            )

            return

        print("\nPOSIÇÕES PROTEGIDAS")

        for posicao in self.__posicoes:

            print(
                f"{posicao.instrumento.codigo} "
                f"- {posicao.quantidade}"
            )
