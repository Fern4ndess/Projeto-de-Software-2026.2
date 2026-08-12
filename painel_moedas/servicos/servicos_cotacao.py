class ServicoCotacao:

    def __init__(self, provedores):

        self.__provedores = tuple(
            provedores
        )

    def obter_cotacao(
        self,
        instrumento,
        moeda_referencia
    ):

        for provedor in self.__provedores:

            try:

                return provedor.obter_cotacao(
                    instrumento,
                    moeda_referencia
                )

            except ValueError:
                continue

        raise ValueError(
            f"Nenhum provedor encontrou "
            f"cotação para "
            f"{instrumento.codigo}."
        )
