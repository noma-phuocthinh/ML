#%%
import pandas as pd
from bs4 import BeautifulSoup

#%%
df =pd.read_csv('dataset/SalesTransactions.csv', encoding='utf-8', dtype='unicode')
print(df)

#%%
df =pd.read_json('dataset/SalesTransactions.json', encoding='utf-8', dtype='unicode')
print(df)

#%%
df = pd.read_csv('dataset/SalesTransactions.txt', encoding='utf-8', dtype='unicode')
print(df)

#%%
with open('dataset/SalesTransactions.xml', 'r', encoding='utf-8') as f:
    data = f.read()

bs_data = BeautifulSoup(data, 'xml')
print(df)

#%%
dataframe = pd.read_excel('dataset/SalesTransactions.xlsx')
print(dataframe)