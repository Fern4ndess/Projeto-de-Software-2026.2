class ErroFinanceiro(Exception):
    """Classe base para erros da carteira."""
    pass

class SaldoInsuficienteError(ErroFinanceiro):
    def __init__(self, saldo_atual, valor_tentado):
        super().__init__(
            f"Saldo insuficiente. Disponível: R$ {saldo_atual:.2f}, "
            f"Tentativa de compra: R$ {valor_tentado:.2f}"
        )

class QuantidadeInvalidaError(ErroFinanceiro):
    def __init__(self, mensagem="A quantidade e o valor devem ser maiores que zero."):
        super().__init__(mensagem)