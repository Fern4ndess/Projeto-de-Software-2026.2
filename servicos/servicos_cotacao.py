from datetime import datetime, timedelta


class ServicoCotacao:

    def __init__(self, provedores, ttl_segundos=30):

        self.__provedores = tuple(provedores)

        # Duração de vida de cada entrada do cache
        self.__ttl = timedelta(seconds=ttl_segundos)

        # Cache: chave -> (Cotacao, momento_em_que_foi_guardada)
        self.__cache = {}

        # contadores só para fins de teste do RF10.
        self.__acertos_cache = 0
        self.__chamadas_reais = 0

    @property
    def acertos_cache(self):
        return self.__acertos_cache

    @property
    def chamadas_reais(self):
        return self.__chamadas_reais

    def __chave_cache(self, instrumento, moeda_referencia):
        return (instrumento.codigo, moeda_referencia.upper())

    def __cache_valido(self, momento_guardado):
        return datetime.now() - momento_guardado < self.__ttl

    def obter_cotacao(self, instrumento, moeda_referencia):
        chave = self.__chave_cache(instrumento, moeda_referencia)

        # 1) Já existe algo em cache e ainda está dentro do TTL?
        if chave in self.__cache:
            cotacao_guardada, momento = self.__cache[chave]

            if self.__cache_valido(momento):
                self.__acertos_cache += 1
                return cotacao_guardada

        # 2) Cache frio ou expirado: busca de verdade nos provedores
        for provedor in self.__provedores:

            try:
                cotacao = provedor.obter_cotacao(
                    instrumento,
                    moeda_referencia
                )

                self.__cache[chave] = (cotacao, datetime.now())
                self.__chamadas_reais += 1

                return cotacao

            except ValueError:
                continue

        raise ValueError(
            f"Nenhum provedor encontrou "
            f"cotação para {instrumento.codigo}."
        )