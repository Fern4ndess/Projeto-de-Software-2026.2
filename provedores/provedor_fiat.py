from datetime import datetime
from decimal import Decimal
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import json

from modelos.cotacao import Cotacao
from modelos.moeda_fiat import MoedaFiat
from modelos.exceptions import AtivoDesconhecidoError
from provedores.provedor_cotacao import ProvedorCotacao


class ProvedorFiat(ProvedorCotacao):

    URL_BASE = "https://api.frankfurter.dev/v2"

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

        moeda_referencia = moeda_referencia.upper()
        codigo = instrumento.codigo.upper()

        if moeda_referencia != "BRL":
            raise ValueError(
                "Nesta etapa a referência é BRL."
            )

        if codigo == "BRL":
            return Cotacao(
                "BRL",
                "BRL",
                Decimal("1.00"),
                datetime.now()
            )

        url = (
            f"{self.URL_BASE}/rate/"
            f"{codigo}/"
            f"{moeda_referencia}"
        )

        requisicao = Request(
            url,
            headers={
                "User-Agent": "Painel-de-Moedas-e-Economia/1.0"
            }
        )

        try:
            with urlopen(
                requisicao,
                timeout=10
            ) as resposta:

                dados = json.loads(
                    resposta.read().decode("utf-8")
                )

        except HTTPError as erro:

            if erro.code == 404:
                raise AtivoDesconhecidoError(
                    codigo
                )

            raise ValueError(
                f"Erro ao consultar a Frankfurter: "
                f"HTTP {erro.code}."
            )

        except URLError as erro:

            raise ValueError(
                "Não foi possível conectar à "
                "Frankfurter."
            ) from erro

        except json.JSONDecodeError as erro:

            raise ValueError(
                "A Frankfurter retornou uma "
                "resposta inválida."
            ) from erro

        if "rate" not in dados:

            raise ValueError(
                "A resposta da Frankfurter não "
                "contém uma cotação válida."
            )

        try:
            valor = Decimal(
                str(dados["rate"])
            )
        except Exception as erro:

            raise ValueError(
                "A cotação retornada pela "
                "Frankfurter é inválida."
            ) from erro

        data_cotacao = dados.get("date")

        if data_cotacao:
            try:
                horario = datetime.fromisoformat(
                    f"{data_cotacao}T00:00:00"
                )
            except ValueError:
                horario = datetime.now()
        else:
            horario = datetime.now()

        return Cotacao(
            codigo,
            moeda_referencia,
            valor,
            horario
        )
