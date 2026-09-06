# (isolar os erros)

class FinanceError(Exception):
    # Classe base para todos os erros financeiros do sistema.
    pass

class InsufficientBalanceError(FinanceError):
    # Lançado quando o usuário tenta vender mais de um ativo do que possui.
    def __init__(self, symbol, available, requested):
        super().__init__(f"Saldo insuficiente para {symbol}. Disponível: {available}, Tentativa de venda: {requested}")

class UnknownAssetError(FinanceError):
    # Lançado quando se tenta negociar um símbolo que não existe
    def __init__(self, symbol):
        super().__init__(f"Ativo desconhecido: {symbol}")