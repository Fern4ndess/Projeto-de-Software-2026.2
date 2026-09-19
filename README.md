# Painel de Moedas e Economia

Projeto desenvolvido em **Python** utilizando **Programação Orientada a Objetos (POO)**.

O sistema representa uma carteira capaz de trabalhar com **moedas fiduciárias e criptoativos**, consultar cotações, registrar posições, realizar operações de compra, calcular volatilidade, analisar risco e converter os valores da carteira para reais.

## Status

**RF1 até RF10 implementados.**

## Tecnologias

- Python 3
- Programação Orientada a Objetos (POO)
- `Decimal` para operações financeiras
- `dataclasses`
- `abc` para abstrações
- PlantUML para o diagrama de classes
- Frankfurter API para cotações de moedas fiduciárias
- CoinGecko API para cotações e histórico de criptoativos

O projeto utiliza apenas recursos da biblioteca padrão do Python. Por isso, não há dependências externas de Python necessárias no `requirements.txt`.

## Requisitos funcionais implementados

| RF | Descrição | Implementação |
|---|---|---|
| RF1 | Cotações imutáveis | Cada consulta gera um objeto `Cotacao` que representa o registro daquela consulta. |
| RF2 | Sem mistura implícita de moedas | A classe `Dinheiro` impede a soma de valores pertencentes a moedas diferentes. |
| RF3 | Moedas fiduciárias e criptoativos | `MoedaFiat` e `Criptoativo` herdam de `Instrumento` e possuem comportamentos próprios. |
| RF4 | Exibição apropriada ao tipo | Moedas fiduciárias são exibidas com duas casas decimais e criptoativos com oito casas decimais. |
| RF5 | Avaliação mista da carteira | A carteira pode possuir diferentes tipos de instrumentos e calcular o valor total em reais. |
| RF6 | Cotações multifonte | `ServicoCotacao` utiliza uma abstração comum de provedores para consultar diferentes fontes. |
| RF7 | Carteira protegida | `CarteiraProtegida` controla saldo, compras e posições, evitando operações inválidas. |
| RF8 | Erros financeiros distinguíveis | O sistema possui exceções específicas para saldo insuficiente, quantidade inválida e ativo desconhecido. |
| RF9 | Análise de risco plugável | O módulo `risk_analyzer` permite selecionar diferentes estratégias de análise de risco em tempo de execução. |
| RF10 | Cache de cotações | `ServicoCotacao` mantém um cache transparente para evitar consultas externas repetidas dentro do período de validade. |

## Arquitetura

O projeto está organizado em três principais camadas:

### `modelos/`

Contém as entidades e regras fundamentais do domínio.

Principais classes:

- `Instrumento`
- `MoedaFiat`
- `Criptoativo`
- `Dinheiro`
- `Cotacao`
- `Posicao`
- `Carteira`
- `CarteiraProtegida`

Também contém as exceções financeiras utilizadas pelo sistema.

### `provedores/`

Responsável pela comunicação com as fontes externas de cotação.

Principais componentes:

- `ProvedorCotacao`
- `ProvedorFiat`
- `ProvedorCripto`

Os provedores possuem uma abstração comum para que o serviço de cotação possa trabalhar com diferentes fontes sem depender diretamente da implementação específica de cada API.

### `servicos/`

Contém as regras de serviço que coordenam o funcionamento da aplicação.

Principais componentes:

- `ServicoCotacao`
- `risk_analyzer.py`

`ServicoCotacao` é responsável por consultar os provedores, controlar o cache de cotações e solicitar o cálculo de volatilidade adequado ao instrumento.

O módulo `risk_analyzer.py` contém as estratégias de análise de risco.

## APIs utilizadas

### Frankfurter

Utilizada para consultar cotações e históricos de **moedas fiduciárias**.

O histórico utilizado para moedas fiduciárias considera uma janela de aproximadamente **30 dias**, conforme o requisito de volatilidade do projeto.

### CoinGecko

Utilizada para consultar cotações e históricos de **criptoativos**.

Para criptoativos, o histórico utilizado para a volatilidade considera preços organizados em intervalos horários dentro de uma janela de aproximadamente **24 horas**.

As consultas às APIs dependem de conexão com a internet.

## Volatilidade

O projeto utiliza como implementação da volatilidade o **desvio-padrão dos retornos percentuais** das cotações.

Para cada instrumento:

- **Moedas fiduciárias:** retornos calculados a partir de cotações diárias.
- **Criptoativos:** retornos calculados a partir de preços horários.

Essa fórmula foi adotada como implementação para atender ao requisito de cálculo de volatilidade, já que o requisito funcional define o período e a frequência das cotações, mas não determina uma fórmula matemática específica.

## Carteira

A carteira trabalha com posições compostas por:

- instrumento;
- quantidade;
- valor correspondente em reais obtido por meio do serviço de cotação.

O cálculo do valor total é feito de forma uniforme, sem a necessidade de criar uma regra específica para cada tipo de ativo.

A `CarteiraProtegida` acrescenta o controle de saldo para operações de compra.

## Tratamento de erros

O projeto possui uma hierarquia própria de erros financeiros:

```text
ErroFinanceiro
├── SaldoInsuficienteError
├── QuantidadeInvalidaError
└── AtivoDesconhecidoError
