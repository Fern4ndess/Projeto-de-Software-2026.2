from decimal import Decimal
from modelos.posicao import Posicao

# EXCEÇÕES DISTINGUÍVEIS
class ErroFinanceiro(Exception):
    # Classe base para erros financeiros distinguíveis do sistema.
    pass

class SaldoInsuficienteError(ErroFinanceiro):
    def __init__(self, saldo_atual, valor_tentado):
        super().__init__(
            f"Saldo insuficiente. Disponível: R$ {saldo_atual:.2f}, "
            f"Tentativa da operação: R$ {valor_tentado:.2f}"
        )

class QuantidadeInvalidaError(ErroFinanceiro):
    def __init__(self, mensagem="A quantidade e o valor devem ser maiores que zero."):
        super().__init__(mensagem)


class CarteiraProtegida:

    def __init__(self, saldo_inicial):
        saldo_inicial = Decimal(str(saldo_inicial))

        if saldo_inicial < Decimal("0"):
            raise QuantidadeInvalidaError("O saldo inicial não pode ser negativo.")

        self.__saldo = saldo_inicial
        self.__posicoes = []

    @property
    def saldo(self):
        return self.__saldo

    def comprar(self, instrumento, quantidade, valor_total):
        quantidade = Decimal(str(quantidade))
        valor_total = Decimal(str(valor_total))

        if quantidade <= Decimal("0"):
            raise QuantidadeInvalidaError("A quantidade deve ser maior que zero.")

        if valor_total <= Decimal("0"):
            raise QuantidadeInvalidaError("O valor da operação deve ser maior que zero.")

        if valor_total > self.__saldo:
            raise SaldoInsuficienteError(self.__saldo, valor_total)

        self.__saldo -= valor_total

        self.__posicoes.append(
            Posicao(
                instrumento,
                quantidade
            )
        )

    def listar_posicoes(self):
        if not self.__posicoes:
            print("\nNenhuma posição cadastrada.")
            return

        print("\nPOSIÇÕES PROTEGIDAS")
        for posicao in self.__posicoes:
            print(f"{posicao.instrumento.codigo} - {posicao.quantidade}")
            
    def obter_posicoes(self):
        return tuple(self.__posicoes)