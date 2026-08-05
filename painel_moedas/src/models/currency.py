from dataclasses import dataclass
from datetime import datetime

# RF1 [E] — Cotações imutáveis. 
# O parâmetro frozen=True garante o Encapsulamento estrito.

@dataclass(frozen=True)
class Cotacao:
    moeda_origem: str
    moeda_destino: str
    valor: float
    timestamp: datetime

    def __post_init__(self):
        """
        Validação de segurança no momento da criação.
        Garante que não existam cotações irreais no sistema.
        """
        if self.valor <= 0:
            raise ValueError(f"Erro: O valor da cotação ({self.valor}) deve ser maior que zero.")
        if self.moeda_origem == self.moeda_destino:
            raise ValueError(f"Erro: Moeda de origem e destino não podem ser iguais.")
