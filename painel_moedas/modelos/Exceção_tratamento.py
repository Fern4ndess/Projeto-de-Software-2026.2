class ErroFinanceiro(Exception):
    """Classe base para todos os erros do Painel de Moedas e Economia."""
    pass

class SaldoInsuficienteError(ErroFinanceiro):
    """Disparada quando o usuário tenta operar sem saldo suficiente (RF8)."""
    def __init__(self, saldo_atual, valor_tentado, moeda="BRL"):
        # Se for cripto, formata com mais casas decimais; se fiduciária, com 2.
        casas = 8 if moeda in ["BTC", "ETH"] else 2
        
        super().__init__(
            f"Saldo insuficiente. Disponível: {moeda} {saldo_atual:.{casas}f}, "
            f"Tentativa: {moeda} {valor_tentado:.{casas}f}"
        )

class AtivoDesconhecidoError(ErroFinanceiro):
    """Disparada quando um símbolo/ticker (ex: ABCX) não existe nas APIs (RF8)."""
    def __init__(self, simbolo):
        super().__init__(f"Ativo desconhecido: O símbolo '{simbolo}' não foi encontrado no sistema.")

class OperacaoMoedaInvalidaError(ErroFinanceiro):
    """Disparada ao tentar operar ou somar moedas diferentes sem conversão (RF2)."""
    def __init__(self, moeda_a, moeda_b):
        super().__init__(
            f"Operação inválida: Não é possível combinar ou somar {moeda_a} e {moeda_b} "
            f"diretamente sem realizar a conversão explícita."
        )

class QuantidadeInvalidaError(ErroFinanceiro):
    """Disparada quando valores ou quantidades são zerados ou negativos."""
    def __init__(self, mensagem="A quantidade e o valor devem ser maiores que zero."):
        super().__init__(mensagem)
      
