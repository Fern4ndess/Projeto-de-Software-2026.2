# Painel de Moedas e Economia

Projeto desenvolvido em **Python** utilizando **Programação Orientada a Objetos (POO)**.

O sistema representa uma carteira com moedas fiduciárias e criptoativos, permitindo trabalhar com cotações, posições, operações financeiras protegidas, análise de risco e cache de cotações.

> **Status: Em desenvolvimento — RF1 até RF10 implementados.**
>
> **Observação:** nesta etapa, as cotações são simuladas com valores fixos. A integração com APIs externas será realizada posteriormente.

## Tecnologias

- Python 3
- Programação Orientada a Objetos
- `Decimal`
- `dataclasses`
- PlantUML

## Requisitos implementados

| RF | Descrição |
|---|---|
| RF1 | Cotações imutáveis |
| RF2 | Sem mistura implícita de moedas |
| RF3 | Moedas fiduciárias e criptoativos |
| RF4 | Exibição apropriada ao tipo |
| RF5 | Avaliação mista da carteira |
| RF6 | Cotações multifonte |
| RF7 | Carteira protegida |
| RF8 | Erros financeiros distinguíveis |
| RF9 | Avaliação de risco plugável |
| RF10 | Cache de cotações invisível |

## Estrutura

```text
painel_moedas/
│
├── modelos/
│   ├── carteira.py
│   ├── cotacao.py
│   ├── criptoativo.py
│   ├── dinheiro.py
│   ├── exceptions.py
│   ├── instrumento.py
│   ├── moeda_fiat.py
│   └── posicao.py
│
├── provedores/
│   ├── provedor_cotacao.py
│   ├── provedor_crypto.py
│   └── provedor_fiat.py
│
├── servicos/
│   ├── risk_analyzer.py
│   └── servicos_cotacao.py
│
├── diagrama/
│   ├── diagrama.puml
│   └── diagrama atualizado2.png
│
├── main.py
├── README.md
├── requirements.txt
└── .gitignore
