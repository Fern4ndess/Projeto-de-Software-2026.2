from datetime import datetime
from decimal import Decimal

from modelos.cotacao import Cotacao
from modelos.criptoativo import Criptoativo

from provedores.provedor_cotacao import (
    ProvedorCotacao
)


class ProvedorCripto(ProvedorCotacao):

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

        if not isinstance(
            instrumento,
            Criptoativo
        ):
            raise ValueError(
                "Este provedor atende apenas "
                "criptoativos."
            )

        if moeda_referencia.upper() != "BRL":
            raise ValueError(
                "Nesta etapa a referência é BRL."
            )

        codigo = instrumento.codigo

        if codigo not in self.__cotacoes:
            raise ValueError(
                f"Não existe cotação simulada "
                f"para {codigo}."
            )

        return Cotacao(
            codigo,
            "BRL",
            self.__cotacoes[codigo],
            datetime.now()
        )
