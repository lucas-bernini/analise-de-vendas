import pandas as pd
from datetime import datetime
import numpy as np

df = pd.read_csv('venda.csv')
print(df.head(10))

#informação dos dados.
df.info()

# Análise dos dados.
print(df.describe(include='all'))

# Substituindo os valores 'ERROR', 'UNKNOWN', 'NaN', '' por NaN.
df.replace(['ERROR', 'UNKNOWN', 'NaN', ''], np.nan, inplace=True)

# Converte para data, caso não esteja no padrão ira ficar como NaT.
df['Transaction Date'] = pd.to_datetime(df['Transaction Date'], errors='coerce')

# Converter as colunas em valor númerico.
colunas = ['Quantity', 'Price Per Unit', 'Total Spent']
df[colunas] = df[colunas].apply(pd.to_numeric, errors='coerce')

# Dicionário com os itens e seus preços correspondentes, retirando valores com preço duplicado.
item_mapping = {
     4 : 'Sandwich',
     1.5 : 'Tea',
     3 : 'Cake',
     1 : 'Cookie',
     5 : 'Salad',
     2 : 'Coffee',
}
#Preencher os valores NaN de 'Price Per Unit' com os valores do dicionário.
df['Item'] = df['Item'].fillna(df['Price Per Unit'].map(item_mapping))

# Dicionário com os itens e seus preços correspondentes.
price_mapping = {
    'Sandwich': 4,
    'Tea': 1.5,
    'Cake': 3,
    'Cookie': 1,
    'Salad': 5,
    'Coffee': 2,
    'Juice': 3,
    'Smoothie': 4
}

# Preencher os valores NaN de 'Price Per Unit' com os valores do dicionário.
df['Price Per Unit'] = df['Price Per Unit'].fillna(df['Item'].map(price_mapping))

#Criar um campo e calcular campos vazios no total spent
df['Total vendido'] = df['Quantity'] * df['Price Per Unit']
mascara = df['Total Spent'].isna() | (df['Total Spent'] != (df['Total vendido']))
df['Total Spent'] = df['Total vendido'].where(mascara, df['Total Spent'])

# Removendo a coluna que foi criada temporariamente.
df.drop(columns=['Total vendido'], inplace=True)

# Removendo registros de linhas vazias, das coluna Transaction ID ou Transaction Date.
df.dropna(subset=['Transaction ID', 'Transaction Date'], inplace=True)

# Adicionando valor com mais frequência nos campos faltantes.
df['Payment Method'] = df['Payment Method'].fillna(df['Payment Method'].mode()[0])
df['Location'] = df['Location'].fillna(df['Location'].mode()[0])

# Removendo registros que constam como NaN dos Itens que não foi possivel tratamento, pois campos preço e valor total estavam vazio, impossibilitando tratamento de outros campos.
df.dropna(subset=['Item', 'Quantity', 'Total Spent'], inplace=True)

df.info()

# Exportar os dados para excel.
df.to_excel('Venda_Cafe.xlsx', index=False)