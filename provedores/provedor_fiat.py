from datetime import datetime
from decimal import Decimal

from modelos.cotacao import Cotacao
from modelos.moeda_fiat import MoedaFiat

from provedores.provedor_cotacao import (
    ProvedorCotacao
)


class ProvedorFiat(ProvedorCotacao):

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

        if not isinstance(
            instrumento,
            MoedaFiat
        ):
            raise ValueError(
                "Este provedor atende apenas "
                "moedas fiduciárias."
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
