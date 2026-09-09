#  Painel de Moedas e Economia

Projeto desenvolvido em **Python** utilizando Programação Orientada a Objetos (POO).

O sistema representa uma carteira com moedas fiduciárias e criptoativos,
trabalhando com cotações, posições e operações financeiras protegidas.

> **Status: Em desenvolvimento — RF1 até RF10**

##  Tecnologias

- Python 3
- Programação Orientada a Objetos
- `Decimal`
- PlantUML

##  Requisitos implementados

| RF | Descrição |
|---|---|
| RF1 | Cotações imutáveis |
| RF2 | Sem mistura implícita de moedas |
| RF3 | Moedas fiduciárias e criptoativos |
| RF4 | Exibição apropriada ao tipo |
| RF5 | Avaliação mista da carteira |
| RF6 | Cotações multifonte |
| RF7 | Carteira protegida |
| RF8 |  Erros financeiros distinguíveis |
| RF9 |   |
| RF10 |  |

##  Estrutura

```text
painel_moedas/
│
├── modelos/
├── provedores/
├── servicos/
├── diagrama/
│   ├── diagrama.puml
│   └── diagrama atualizado2.png
│
├── main.py
├── README.md
├── requirements.txt
└── .gitignore
