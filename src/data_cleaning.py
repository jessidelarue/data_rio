import pandas as pd

# Carregar o arquivo Excel, ignorando as primeiras 4 linhas e selecionando as linhas 5 a 18
xls_file_path = 'data\ccbb.xls'
df = pd.read_excel(xls_file_path, skiprows=4, nrows=13)  # Lê apenas as linhas 5 a 18

df.columns = ["Mês", "2015", "2016", "2017", "2018", "2019", "2020", "2021"]

df = df.drop(index=0)

# Remover quaisquer linhas vazias ou indesejadas (apenas por precaução)
#df = df.dropna(how="all")

# Função para formatar os números, removendo espaços e decimais
def format_number(value):
    try:
        # Remove espaços e a parte decimal ('.0'), e converte para inteiro
        value = str(value).replace(' ', '').replace('.0', '')
        return int(value)
    except ValueError:
        return None  # ou np.nan caso haja valores inválidos

# Mantém a coluna "Mês" e aplica a função apenas nas colunas dos anos
years = ['2015', '2016', '2017', '2018', '2019', '2020', '2021']
df[years] = df[years].applymap(format_number)

# Salvar o DataFrame como CSV
csv_file_path = 'data\ccbb.csv'
df.to_csv(csv_file_path, index=False)

print(f"Arquivo CSV salvo em: {csv_file_path}")

