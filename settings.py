#app configuratin
app_files_dir = './files/'
gnucash_database_path = '...'

# date to retrieve info
date = '2020-02-28'

# B3 commodities
B3_commodities = ['ACAO']

# Funds commodities
CVM_Funds_commodities = ['FUNDO RF','FUNDO MULTI','PREVIDENCIA']

#CVM configuration
cvm_funds_url = 'http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{YYYYMM}.csv'

#B3 configuratin
b3_urlBase = 'http://bvmf.bmfbovespa.com.br//InstDados/SerHist/'
b3_fileNameBase = 'COTAHIST_M{PERIODO}.ZIP'