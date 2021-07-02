# -*- coding: utf-8 -*-
"""project1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12K_Qxrj87_UCNhRHetkoQDYanU0M5kRM
"""

import numpy as np
import pandas as pd
import requests
import xlsxwriter
import math

stonks=pd.read_csv("sp_500_stocks.csv")
stonks

from secrets import IEX_CLOUD_API_TOKEN

symbol = 'AAPL'
api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/quote/?token={IEX_CLOUD_API_TOKEN}'
data = requests.get(api_url).json()
print(data)

price = data['latestPrice']
print(price)
market_cap = data['marketCap']
print(market_cap)

my_columns = ['Ticker','price', 'market capitalization','stocks to buy']
output_dataframe = pd.DataFrame(columns = my_columns)
output_dataframe

output_dataframe.append( pd.Series([symbol, price,     market_cap,     'NaN'] , index = my_columns),
    ignore_index=True    
)

output_dataframe=pd.DataFrame(columns = my_columns)

for stock in stonks['Ticker']:
    api_url = f'https://sandbox.iexapis.com/stable/stock/{stock}/quote/?token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(api_url).json()
    output_dataframe=output_dataframe.append(
    pd.Series([
    stock,
    data['latestPrice'],
    data['marketCap'],
    'N/A'    
],
    index = my_columns
    ),
    ignore_index = True
)
    output_dataframe

output_dataframe

def divide_chunks(l, n):
      
    # looping till length l
    for i in range(0, len(l), n): 
        yield l[i:i + n]

ticker_group = list(divide_chunks(stonks["Ticker"],100))
#ticker_group

symbol_strings = []
for i in range(0,len(ticker_group)):
    symbol_strings.append(','.join(ticker_group[i]))
    #print(symbol_strings[i])
output_dataframe = pd.DataFrame(columns = my_columns)
for symbol_string in symbol_strings:
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(batch_api_call_url).json()
    for symbol in symbol_string.split(','):
        output_dataframe = output_dataframe.append(
        pd.Series(
        [
            symbol, 
            data[symbol]['quote']['latestPrice'],
            data[symbol]['quote']['marketCap'],
            'N/A'
        ],  index = my_columns),
            ignore_index = True     
        )
output_dataframe

portfolio_size = input('enter portfolio size in integers')

try :
    val = float(portfolio_size)
except ValueError:
    print('please enter integers only')
    portfolio_size = input('enter portfolio size in integers')
    val = float(portfolio_size)

weight_of_stock = val/len(output_dataframe.index)
print(weight_of_stock)

#no_of_shares_to_buy = weight_of_stock/stock_price

for i in range(0,len(output_dataframe.index)):
    output_dataframe.loc[i,'stocks to buy'] = math.floor(weight_of_stock/output_dataframe.loc[i,'price'])
output_dataframe

writer = pd.ExcelWriter('recommended stocks.xlsx', engine = 'xlsxwriter')
output_dataframe.to_excel(writer, 'recommended stocks', index = False)

background_color = '#0a0a23'
font_color = '#ffffff'

string_format  = writer.book.add_format(
    {
        'font_color' : font_color,
        'bg_color' : background_color,
        'border' : 1
    }
 )
dollar_format  = writer.book.add_format(
    {
        
        'font_color' : font_color,
        'bg_color' : background_color,
        'border' : 1,
        'num_format' :'$0.00'
    }
 )
integer_format  = writer.book.add_format(
    {
        
        'font_color' : font_color,
        'bg_color' :  background_color,
        'border' : 1,
        'num_format' : '0'
    }
 )

# writer.sheets['recommended stocks'].set_column('A:A', 18, string_format)
# writer.sheets['recommended stocks'].set_column('B:B', 18, string_format)
# writer.sheets['recommended stocks'].set_column('C:C', 18, string_format)
# writer.sheets['recommended stocks'].set_column('D:D', 18, string_format)
# writer.save()

column_format ={
    'A': ['Ticker', string_format],
    'B': ['price', dollar_format],
    'C': ['market capitalization', integer_format],
    'D': ['stocks to buy', integer_format]    
}

for column in column_format.keys():
    writer.sheets['recommended stocks'].set_column(f'{column}:{column}' , 18, column_format[column][1])
    writer.sheets['recommended stocks'].write(f'{column}1', f'{column_format[column][0]}')
writer.save()

