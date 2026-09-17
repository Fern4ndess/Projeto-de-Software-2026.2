import json
from datetime import datetime
from decimal import Decimal
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from modelos.cotacao import Cotacao
from modelos.criptoativo import Criptoativo
from modelos.exceptions import AtivoDesconhecidoError
from provedores.provedor_cotacao import ProvedorCotacao


class ProvedorCripto(ProvedorCotacao):

    URL_BASE = "https://api.coingecko.com/api/v3"

    def __init__(self):
        self.api_key = "CG-FJ665ewLg6r9QFoPT1GaCWRz"

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

        moeda_referencia = moeda_referencia.upper()
        codigo = instrumento.codigo.upper()

        if moeda_referencia != "BRL":
            raise ValueError(
                "Nesta etapa a referência é BRL."
            )

        parametros = urlencode({
            "vs_currency": moeda_referencia.lower(),
            "symbols": codigo.lower(),
            "include_tokens": "top"
        })

        url = (
            f"{self.URL_BASE}/coins/markets?"
            f"{parametros}"
        )

        requisicao = Request(
            url,
            headers={
                "User-Agent": "Painel-de-Moedas-e-Economia/1.0",
                "x-cg-demo-api-key": self.api_key
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

            if erro.code in (401, 403):
                raise ValueError(
                    "A chave da CoinGecko é inválida "
                    "ou não possui acesso à API."
                )

            try:
                mensagem = erro.read().decode(
                    "utf-8"
                )
            except Exception:
                mensagem = ""

            raise ValueError(
                f"Erro ao consultar a CoinGecko: "
                f"HTTP {erro.code}. "
                f"{mensagem}"
            )

        except URLError as erro:

            raise ValueError(
                "Não foi possível conectar à CoinGecko."
            ) from erro

        except json.JSONDecodeError as erro:

            raise ValueError(
                "A CoinGecko retornou uma "
                "resposta inválida."
            ) from erro

        if not dados:
            raise AtivoDesconhecidoError(codigo)

        moeda = dados[0]

        if "current_price" not in moeda:
            raise ValueError(
                "A CoinGecko não retornou "
                "uma cotação válida."
            )

        try:

            valor = Decimal(
                str(moeda["current_price"])
            )

        except Exception as erro:

            raise ValueError(
                "A cotação retornada pela "
                "CoinGecko é inválida."
            ) from erro

        return Cotacao(
            codigo,
            moeda_referencia,
            valor,
            datetime.now()
        )
