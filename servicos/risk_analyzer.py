from abc import ABC, abstractmethod
from modelos.carteira import Portfolio # Assumindo que a classe da carteira se chama Portfolio

class RiskStrategy(ABC):
    @abstractmethod
    def evaluate_risk(self, portfolio: Portfolio) -> str:
        """Avalia a carteira e retorna uma string (ex: BAIXO, MODERADO, ALTO)"""
        pass

class ConservativeRiskModel(RiskStrategy):
    def evaluate_risk(self, portfolio: Portfolio) -> str:
        # Penaliza criptomoedas fortemente
        crypto_ratio = portfolio.get_crypto_percentage()
        if crypto_ratio > 0.10: # Mais de 10% em cripto é inaceitável para conservadores
            return "ALTO"
        elif crypto_ratio > 0.0:
            return "MODERADO"
        return "BAIXO"

class AggressiveRiskModel(RiskStrategy):
    def evaluate_risk(self, portfolio: Portfolio) -> str:
        # Penaliza apenas concentração em um único ativo, mas tolera cripto[cite: 2]
        max_concentration = portfolio.get_highest_asset_concentration()
        if max_concentration > 0.60: # Mais de 60% em um único ativo
            return "ALTO"
        elif max_concentration > 0.40:
            return "MODERADO"
        return "BAIXO"

# O uso na carteira ficaria assim:
# risk = model.evaluate_risk(minha_carteira)