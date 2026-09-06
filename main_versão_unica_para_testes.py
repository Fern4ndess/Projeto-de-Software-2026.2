from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation


# ============================================================
# RF1 - COTAÇÃO IMUTÁVEL
# ============================================================

@dataclass(frozen=True)
class Cotacao:
    """
    RF1 [E]
    Uma cotação, depois de criada, não pode ser alterada.
    """

    moeda_origem: str
    moeda_destino: str
    valor: Decimal
    horario: datetime

    def __post_init__(self):
        object.__setattr__(
            self,
            "moeda_origem",
            self.moeda_origem.upper()
        )

        object.__setattr__(
            self,
            "moeda_destino",
            self.moeda_destino.upper()
        )

        if self.valor <= Decimal("0"):
            raise ValueError(
                "O valor da cotação deve ser maior que zero."
            )

    def __str__(self):
        return (
            f"1 {self.moeda_origem} = "
            f"{self.valor:.2f} {self.moeda_destino} "
            f"(registrada às "
            f"{self.horario.strftime('%H:%M:%S')})"
        )


# ============================================================
# RF2 - DINHEIRO
# ============================================================

class Dinheiro:
    """
    RF2 [E]
    Representa um valor monetário associado a uma moeda.
    Não permite soma direta entre moedas diferentes.
    """

    def __init__(self, valor, moeda):

        self.__valor = Decimal(str(valor))
        self.__moeda = moeda.upper()

        if self.__valor < Decimal("0"):
            raise ValueError(
                "O valor monetário não pode ser negativo."
            )

    @property
    def valor(self):
        return self.__valor

    @property
    def moeda(self):
        return self.__moeda

    def __add__(self, outro):

        if not isinstance(outro, Dinheiro):
            raise TypeError(
                "A operação exige outro objeto Dinheiro."
            )

        if self.moeda != outro.moeda:
            raise ValueError(
                f"Não é possível somar "
                f"{self.moeda} com {outro.moeda}. "
                f"Faça uma conversão explícita."
            )

        return Dinheiro(
            self.valor + outro.valor,
            self.moeda
        )

    def converter(self, cotacao):
        """
        Conversão explícita de uma moeda para outra.
        """

        if self.moeda != cotacao.moeda_origem:
            raise ValueError(
                "A moeda do valor não corresponde "
                "à moeda de origem da cotação."
            )

        novo_valor = self.valor * cotacao.valor

        return Dinheiro(
            novo_valor,
            cotacao.moeda_destino
        )

    def __str__(self):
        return f"{self.valor:.2f} {self.moeda}"


# ============================================================
# RF3 - INSTRUMENTO
# ============================================================

class Instrumento(ABC):
    """
    Classe abstrata base para os instrumentos.
    """

    def __init__(self, codigo):
        self._codigo = codigo.upper()

    @property
    def codigo(self):
        return self._codigo

    @abstractmethod
    def calcular_volatilidade(self):
        pass

    @abstractmethod
    def formatar_valor(self, valor):
        pass


# ============================================================
# RF3/RF4 - MOEDA FIDUCIÁRIA
# ============================================================

class MoedaFiat(Instrumento):

    def calcular_volatilidade(self):
        return (
            "Critério: cotações diárias em uma "
            "janela de 30 dias."
        )

    def formatar_valor(self, valor):

        valor = Decimal(str(valor))

        return (
            f"R$ {valor:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

    def __str__(self):
        return f"{self.codigo} - Moeda fiduciária"


# ============================================================
# RF3/RF4 - CRIPTOATIVO
# ============================================================

class Criptoativo(Instrumento):

    def calcular_volatilidade(self):
        return (
            "Critério: preços horários em uma "
            "janela de 24 horas."
        )

    def formatar_valor(self, valor):

        valor = Decimal(str(valor))

        return f"{valor:.8f} {self.codigo}"

    def __str__(self):
        return f"{self.codigo} - Criptoativo"


# ============================================================
# RF6 - PROVEDOR DE COTAÇÃO
# ============================================================

class ProvedorCotacao(ABC):

    @abstractmethod
    def obter_cotacao(
        self,
        instrumento,
        moeda_referencia
    ):
        pass


# ============================================================
# RF6 - PROVEDOR FIAT SIMULADO
# ============================================================

class ProvedorFiat(ProvedorCotacao):
    """
    Fonte simulada para testes.
    NÃO utiliza API.
    """

    def __init__(self):

        self.__cotacoes = {
            "BRL": Decimal("1.00"),
            "USD": Decimal("5.43"),
            "EUR": Decimal("6.10"),
            "GBP": Decimal("7.20")
        }

    def obter_cotacao(
        self,
        instrumento,
        moeda_referencia
    ):

        if not isinstance(instrumento, MoedaFiat):
            raise ValueError(
                "Este provedor atende apenas moedas fiduciárias."
            )

        codigo = instrumento.codigo

        if moeda_referencia.upper() != "BRL":
            raise ValueError(
                "Nesta etapa a referência é BRL."
            )

        if codigo not in self.__cotacoes:
            raise ValueError(
                f"Não existe cotação simulada para {codigo}."
            )

        return Cotacao(
            codigo,
            "BRL",
            self.__cotacoes[codigo],
            datetime.now()
        )


# ============================================================
# RF6 - PROVEDOR CRIPTO SIMULADO
# ============================================================

class ProvedorCripto(ProvedorCotacao):
    """
    Fonte simulada para testes.
    NÃO utiliza API.
    """

    def __init__(self):

        self.__cotacoes = {
            "BTC": Decimal("600000.00"),
            "ETH": Decimal("30000.00"),
            "SOL": Decimal("800.00")
        }

    def obter_cotacao(
        self,
        instrumento,
        moeda_referencia
    ):

        if not isinstance(instrumento, Criptoativo):
            raise ValueError(
                "Este provedor atende apenas criptoativos."
            )

        codigo = instrumento.codigo

        if moeda_referencia.upper() != "BRL":
            raise ValueError(
                "Nesta etapa a referência é BRL."
            )

        if codigo not in self.__cotacoes:
            raise ValueError(
                f"Não existe cotação simulada para {codigo}."
            )

        return Cotacao(
            codigo,
            "BRL",
            self.__cotacoes[codigo],
            datetime.now()
        )


# ============================================================
# RF6 - SERVIÇO DE COTAÇÃO
# ============================================================

class ServicoCotacao:

    def __init__(self, provedores):
        self.__provedores = provedores

    def obter_cotacao(
        self,
        instrumento,
        moeda_referencia
    ):

        for provedor in self.__provedores:

            try:

                return provedor.obter_cotacao(
                    instrumento,
                    moeda_referencia
                )

            except ValueError:
                continue

        raise ValueError(
            f"Nenhum provedor encontrou "
            f"cotação para {instrumento.codigo}."
        )


# ============================================================
# RF5 - POSIÇÃO
# ============================================================

class Posicao:

    def __init__(self, instrumento, quantidade):

        quantidade = Decimal(str(quantidade))

        if quantidade <= Decimal("0"):
            raise ValueError(
                "A quantidade deve ser maior que zero."
            )

        self.__instrumento = instrumento
        self.__quantidade = quantidade

    @property
    def instrumento(self):
        return self.__instrumento

    @property
    def quantidade(self):
        return self.__quantidade

    def valor_em_reais(self, servico):

        cotacao = servico.obter_cotacao(
            self.instrumento,
            "BRL"
        )

        return self.quantidade * cotacao.valor


# ============================================================
# RF5 - CARTEIRA
# ============================================================

class Carteira:

    def __init__(self):
        self.__posicoes = []

    def adicionar_posicao(
        self,
        instrumento,
        quantidade
    ):

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

            instrumento = posicao.instrumento

            valor = posicao.valor_em_reais(
                servico
            )

            print(
                f"{instrumento.codigo:<6} | "
                f"Quantidade: {posicao.quantidade:<12} | "
                f"Valor em BRL: R$ {valor:,.2f}"
            )

        print("-" * 65)

        total = self.calcular_total(servico)

        print(
            f"TOTAL DA CARTEIRA: R$ {total:,.2f}"
        )


# ============================================================
# RF7 - CARTEIRA PROTEGIDA
# ============================================================

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

    @property
    def saldo(self):
        return self.__saldo

    def comprar(
        self,
        instrumento,
        quantidade,
        valor_total
    ):

        quantidade = Decimal(str(quantidade))
        valor_total = Decimal(str(valor_total))

        if quantidade <= Decimal("0"):
            raise ValueError(
                "A quantidade deve ser maior que zero."
            )

        if valor_total <= Decimal("0"):
            raise ValueError(
                "O valor da operação deve ser maior que zero."
            )

        if valor_total > self.__saldo:
            raise ValueError(
                "Saldo insuficiente."
            )

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

            print(
                f"{posicao.instrumento.codigo} "
                f"- {posicao.quantidade}"
            )


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def pausar():

    input(
        "\nPressione ENTER para continuar..."
    )


def titulo(texto):

    print("\n" + "=" * 65)
    print(texto.center(65))
    print("=" * 65)


def ler_decimal(mensagem):

    while True:

        entrada = input(mensagem).strip()

        try:

            valor = Decimal(
                entrada.replace(",", ".")
            )

            return valor

        except InvalidOperation:

            print(
                "Valor inválido. "
                "Digite um número."
            )


def ler_inteiro(mensagem):

    while True:

        entrada = input(mensagem).strip()

        try:
            return int(entrada)

        except ValueError:

            print(
                "Digite um número inteiro válido."
            )


# ============================================================
# CRIAÇÃO DE INSTRUMENTOS
# ============================================================

def escolher_instrumento():

    print("\nEscolha o instrumento:")

    print("1 - BRL")
    print("2 - USD")
    print("3 - EUR")
    print("4 - GBP")
    print("5 - BTC")
    print("6 - ETH")
    print("7 - SOL")

    opcao = input("\nOpção: ").strip()

    instrumentos = {
        "1": MoedaFiat("BRL"),
        "2": MoedaFiat("USD"),
        "3": MoedaFiat("EUR"),
        "4": MoedaFiat("GBP"),
        "5": Criptoativo("BTC"),
        "6": Criptoativo("ETH"),
        "7": Criptoativo("SOL")
    }

    if opcao not in instrumentos:

        print("Instrumento inválido.")

        return None

    return instrumentos[opcao]


# ============================================================
# MENU RF1
# ============================================================

def menu_rf1():

    titulo("RF1 - COTAÇÕES IMUTÁVEIS")

    instrumento = escolher_instrumento()

    if instrumento is None:
        return

    valor = ler_decimal(
        "\nInforme a cotação em BRL: "
    )

    cotacao = Cotacao(
        instrumento.codigo,
        "BRL",
        valor,
        datetime.now()
    )

    print("\nCotação criada:")
    print(cotacao)

    print(
        "\nA cotação foi registrada como "
        "um objeto imutável."
    )

    print(
        "Uma nova cotação deverá gerar "
        "um novo registro."
    )


# ============================================================
# MENU RF2
# ============================================================

def menu_rf2():

    titulo("RF2 - VALORES MONETÁRIOS")

    print("PRIMEIRO VALOR")

    valor1 = ler_decimal(
        "Digite o valor: "
    )

    moeda1 = input(
        "Digite a moeda (BRL/USD/EUR): "
    ).upper()

    print("\nSEGUNDO VALOR")

    valor2 = ler_decimal(
        "Digite o valor: "
    )

    moeda2 = input(
        "Digite a moeda (BRL/USD/EUR): "
    ).upper()

    dinheiro1 = Dinheiro(
        valor1,
        moeda1
    )

    dinheiro2 = Dinheiro(
        valor2,
        moeda2
    )

    print("\nValores informados:")
    print("1º:", dinheiro1)
    print("2º:", dinheiro2)

    try:

        resultado = dinheiro1 + dinheiro2

        print("\nSoma realizada:")
        print(resultado)

    except ValueError as erro:

        print("\nOPERAÇÃO BLOQUEADA")
        print(erro)

        print(
            "\nPara somar moedas diferentes, "
            "é necessária uma conversão explícita."
        )


# ============================================================
# MENU RF3
# ============================================================

def menu_rf3():

    titulo("RF3 - FAMÍLIAS DE INSTRUMENTOS")

    instrumento = escolher_instrumento()

    if instrumento is None:
        return

    print("\nInstrumento selecionado:")
    print(instrumento)

    print(
        "\nClasse:",
        instrumento.__class__.__name__
    )

    print(
        "Código:",
        instrumento.codigo
    )

    if isinstance(
        instrumento,
        MoedaFiat
    ):

        print(
            "Família: Moeda fiduciária"
        )

    elif isinstance(
        instrumento,
        Criptoativo
    ):

        print(
            "Família: Criptoativo"
        )


# ============================================================
# MENU RF4
# ============================================================

def menu_rf4():

    titulo("RF4 - VOLATILIDADE E FORMATAÇÃO")

    instrumento = escolher_instrumento()

    if instrumento is None:
        return

    valor = ler_decimal(
        "\nDigite um valor para formatação: "
    )

    print("\nInstrumento:")
    print(instrumento)

    print(
        "\nValor formatado:"
    )

    print(
        instrumento.formatar_valor(valor)
    )

    print(
        "\nCritério de volatilidade:"
    )

    print(
        instrumento.calcular_volatilidade()
    )


# ============================================================
# MENU RF5
# ============================================================

def menu_rf5(servico, carteira):

    while True:

        titulo("RF5 - CARTEIRA")

        print("1 - Adicionar posição")
        print("2 - Visualizar carteira")
        print("3 - Calcular total")
        print("0 - Voltar")

        opcao = input(
            "\nEscolha: "
        ).strip()

        if opcao == "1":

            instrumento = escolher_instrumento()

            if instrumento is None:
                pausar()
                continue

            quantidade = ler_decimal(
                "Digite a quantidade: "
            )

            try:

                carteira.adicionar_posicao(
                    instrumento,
                    quantidade
                )

                print(
                    "\nPosição adicionada com sucesso."
                )

            except ValueError as erro:

                print(
                    "\nErro:",
                    erro
                )

            pausar()

        elif opcao == "2":

            carteira.exibir(servico)
            pausar()

        elif opcao == "3":

            total = carteira.calcular_total(
                servico
            )

            print(
                f"\nTotal da carteira: "
                f"R$ {total:,.2f}"
            )

            pausar()

        elif opcao == "0":

            break

        else:

            print("\nOpção inválida.")
            pausar()


# ============================================================
# MENU RF6
# ============================================================

def menu_rf6(servico):

    titulo("RF6 - PROVEDORES DE COTAÇÃO")

    instrumento = escolher_instrumento()

    if instrumento is None:
        return

    try:

        cotacao = servico.obter_cotacao(
            instrumento,
            "BRL"
        )

        print("\nCotação encontrada:")
        print(cotacao)

        print(
            "\nFonte: provedor simulado"
        )

        print(
            "Nenhuma API está sendo utilizada."
        )

    except ValueError as erro:

        print(
            "\nErro:",
            erro
        )


# ============================================================
# MENU RF7
# ============================================================

def menu_rf7():

    titulo("RF7 - CARTEIRA PROTEGIDA")

    saldo = ler_decimal(
        "Digite o saldo inicial: R$ "
    )

    try:

        carteira = CarteiraProtegida(
            saldo
        )

    except ValueError as erro:

        print("\nErro:", erro)
        return

    while True:

        print("\nSaldo atual:")
        print(
            f"R$ {carteira.saldo:,.2f}"
        )

        print("\n1 - Comprar ativo")
        print("2 - Ver posições")
        print("0 - Voltar")

        opcao = input(
            "\nEscolha: "
        ).strip()

        if opcao == "1":

            instrumento = escolher_instrumento()

            if instrumento is None:
                pausar()
                continue

            quantidade = ler_decimal(
                "Digite a quantidade: "
            )

            valor = ler_decimal(
                "Digite o valor da compra: R$ "
            )

            try:

                carteira.comprar(
                    instrumento,
                    quantidade,
                    valor
                )

                print(
                    "\nCompra realizada."
                )

                print(
                    f"Saldo restante: "
                    f"R$ {carteira.saldo:,.2f}"
                )

            except ValueError as erro:

                print(
                    "\nOPERAÇÃO RECUSADA"
                )

                print(erro)

            pausar()

        elif opcao == "2":

            carteira.listar_posicoes()
            pausar()

        elif opcao == "0":

            break

        else:

            print("\nOpção inválida.")
            pausar()


# ============================================================
# MENU DE FUTUROS RFs
# ============================================================

def menu_futuros():

    titulo("PRÓXIMOS REQUISITOS")

    print(
        "O projeto continua em desenvolvimento."
    )

    print("\nNovos RFs serão adicionados futuramente.")

    print(
        "\nAs APIs ainda NÃO fazem parte "
        "desta etapa."
    )

    print(
        "\nFrankfurter e CoinGecko serão "
        "consideradas somente quando "
        "forem solicitadas pela especificação."
    )


# ============================================================
# MENU PRINCIPAL
# ============================================================

def menu_principal():

    # Fontes simuladas.
    # Não há conexão com APIs.

    provedor_fiat = ProvedorFiat()
    provedor_cripto = ProvedorCripto()

    servico = ServicoCotacao(
        [
            provedor_fiat,
            provedor_cripto
        ]
    )

    carteira = Carteira()

    while True:

        titulo(
            "PAINEL DE MOEDAS E ECONOMIA"
        )

        print("\nREQUISITOS FUNCIONAIS\n")

        print(
            "[1] RF1 - Cotações imutáveis"
        )

        print(
            "[2] RF2 - Valores monetários"
        )

        print(
            "[3] RF3 - Instrumentos"
        )

        print(
            "[4] RF4 - Volatilidade e formatação"
        )

        print(
            "[5] RF5 - Carteira"
        )

        print(
            "[6] RF6 - Provedores"
        )

        print(
            "[7] RF7 - Carteira protegida"
        )

        print(
            "\n[8] Próximos requisitos"
        )

        print(
            "[0] Sair"
        )

        print("\n" + "-" * 65)

        opcao = input(
            "Digite a opção: "
        ).strip()

        if opcao == "1":

            menu_rf1()
            pausar()

        elif opcao == "2":

            menu_rf2()
            pausar()

        elif opcao == "3":

            menu_rf3()
            pausar()

        elif opcao == "4":

            menu_rf4()
            pausar()

        elif opcao == "5":

            menu_rf5(
                servico,
                carteira
            )

        elif opcao == "6":

            menu_rf6(servico)
            pausar()

        elif opcao == "7":

            menu_rf7()

        elif opcao == "8":

            menu_futuros()
            pausar()

        elif opcao == "0":

            print(
                "\nSistema encerrado."
            )

            break

        else:

            print(
                "\nOpção inválida."
            )

            pausar()


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    menu_principal()
