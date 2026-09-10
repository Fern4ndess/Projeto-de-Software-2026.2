from datetime import datetime, timedelta


class ServicoCotacao:

    def __init__(self, provedores, validade_cache_segundos=60):
        self.__provedores = tuple(provedores)
        self.__cache = {}
        self.__validade_cache = timedelta(
            seconds=validade_cache_segundos
        )

    def obter_cotacao(self, instrumento, moeda_referencia):

        chave = (
            instrumento.codigo,
            moeda_referencia.upper()
        )

        agora = datetime.now()

        # Verifica se existe uma cotação armazenada
        if chave in self.__cache:

            cotacao, horario_cache = self.__cache[chave]

            # Verifica se o cache ainda é válido
            if agora - horario_cache < self.__validade_cache:
                return cotacao

            # Cache expirado
            del self.__cache[chave]

        # Consulta os provedores
        for provedor in self.__provedores:

            try:
                cotacao = provedor.obter_cotacao(
                    instrumento,
                    moeda_referencia
                )

                # Armazena a nova cotação
                self.__cache[chave] = (
                    cotacao,
                    agora
                )

                return cotacao

            except ValueError:
                continue

        raise ValueError(
            f"Nenhum provedor encontrou cotação para "
            f"{instrumento.codigo}."
        )
