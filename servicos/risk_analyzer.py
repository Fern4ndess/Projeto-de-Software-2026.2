from modelos.criptoativo import Criptoativo

# ESTRATÉGIAS (funções simples, sem classes)

def modelo_conservador(carteira, servico_cotacao) -> str:
    # Estratégia Conservadora: Penaliza qualquer exposição a criptomoedas.
    # Uma carteira com cripto pontua 'MODERADO' sob este modelo.
    posicoes = carteira.obter_posicoes()
    if not posicoes:
        return "BAIXO"
        
    for posicao in posicoes:
        # Se encontrar qualquer criptoativo, o risco sobe para MODERADO
        if isinstance(posicao.instrumento, Criptoativo):
            return "MODERADO"
            
    return "BAIXO"

def modelo_agressivo(carteira, servico_cotacao) -> str:
    posicoes = carteira.obter_posicoes()
    if not posicoes:
        return "BAIXO"

    saldo_livre = carteira.saldo
    valor_investido = sum(p.valor_em_reais(servico_cotacao) for p in posicoes)
    patrimonio_total = saldo_livre + valor_investido
    
    if patrimonio_total == 0:
        return "BAIXO"
        
    for posicao in posicoes:
        concentracao = posicao.valor_em_reais(servico_cotacao) / patrimonio_total
        # Penaliza se mais de 60% do patrimônio estiver em um único ativo
        if concentracao > 0.60:
            return "ALTO"
            
    return "BAIXO"


# CONTEXTO 
def avaliar_carteira(carteira, servico_cotacao, estrategia=modelo_conservador) -> str:
    return estrategia(carteira, servico_cotacao)