import pandas as pd
import numpy as np
import psycopg2 as pg

conexao = pg.connect(
    database = 'db_cnab',
    port = 5432,
    user = 'naymi',
    password='1234'
)

columns=['Tipo', 'Data',  'Valor', 'CPF', 'Cartão', 'Hora', 'Dono da loja', 'Nome_loja']
data = pd.read_fwf('CNAB.txt', names = columns , widths=[1,8,10,11,12,6,14,19], header=None, index_col=None)
print(data)


value = data.groupby('Tipo').agg({'Valor':'sum', 'Nome_loja': 'sum'})

value = value.sort_values(by=['Valor'], 
                      axis=0, 
                      ascending=True,  
                      ignore_index=False)

value = value.reset_index()
print(value)