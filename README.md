# GnuCash Prices Updater

## Objetivo e Motivação

Este script foi criado para auxiliar na obtenção de cotação de ações (ou qualquer ativo negociado na [B3](https://www.b3.com.br) e de cotas de fundos de investimentos (via arquivos da CVM) para importação automática no [GnuCash](https://www.gnucash.org).

Premissa: arquivo do GnuCash deve estar salvo no formato SQLite (o padrão é XML).

*OBS: Tem muito tempo que não programo (pelo menos a lógica ainda está fresca). Meu conhecimento em Python tende a ZERO. Portanto, ignore eventuais atrocidades no código.*

## Instruções

### Configuração de uso

No GnuCash, informar os seguintes dados:

- Fundos de Investimento:
  - Agrupamentos: FUNDO RF, FUNDO MULTI ou PREVIDENCIA
  - Informar o CNPJ como Símbolo/Abreviatura (formatado 00.000.000/0000-00)
- Ações, FIIs de mais ativos negociado na B3:
  - Agrupamento: ACAO
  - Informar o ticker do ativo como Símbolo/Abreviatura. Ex: PETR4
- Títulos do Tesouro Direto:
  - Agrupamentos: Tesouro Direto
  - Informar um dos títulos abaixo separado da data de vencimento por ':' como Símbolo/Abreviatura (formatado titulo:DD/MM/AAAA - Ex: Tesouro IPCA+:15/05/2035):
    - Tesouro IGPM+ com Juros Semestrais
    - Tesouro IPCA+
    - Tesouro IPCA+ com Juros Semestrais
    - Tesouro Prefixado
    - Tesouro Prefixado com Juros Semestrais
    - Tesouro Selic

### Configuração da aplicação

O arquivo *settings.py.template* deve ser renomeado para *settings.py*

As configurações devem ser definidas no arquivo *settings.py*:

```python
#app configuration
app_files_dir = './files/'
gnucash_database_path = "/caminho/para/arquivo.gnucash"

# B3 commodities
B3_commodities = ['ACAO']

# Funds commodities
CVM_Funds_commodities = ['FUNDO RF','FUNDO MULTI','PREVIDENCIA']

# Tesouro Direto commodities
TD_commodities = ['Tesouro Direto']

```

### Forma de Uso

Dentro do arquivo *settings.py* alterar a variável *dates* para os valores desejados. (caso deseje, pode ser alterado para receber o valor da linha de comando)

```python
dates = ['YYYY-MM-DD','YYYY-MM-DD']
```

Esse é o único dado de entrada do usuário e não há qualquer tratamento/validação sobre ele. Informar os valores corretos!

`
python main.py
`

### Importante

No momento, a sequencia é de download do arquivo da CVM, depois da B3 e depois do Tesouro Direto. Não coloquei opção de ativas/desativar um ou outro.

### Saída

Tabela *price*  do GnuCash atualizada com os valores encontrados na data informada.
