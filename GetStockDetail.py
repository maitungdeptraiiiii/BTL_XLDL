import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from yahooquery import Ticker
import requests
from GetStockName import *
import os

def get_stocks_names():
    url = "https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue#See_also"
    tables = pd.read_html(url)
    # Chuyển dữ liệu từ bảng đầu tiên thành DataFrame
    df = pd.DataFrame(tables[0])
    # Lọc các công ty có trụ sở tại Mỹ
    us_companies = df[df[('Headquarters[note 1]', 'Headquarters[note 1]')] == 'United States']
    # Sắp xếp theo lợi nhuận giảm dần và lấy Top 10 công ty có lợi nhuận cao nhất
    top_10_profit_us = us_companies.sort_values(by=('Revenue', 'USD millions'), ascending=False).head(10)
    company_names = top_10_profit_us[('Ram', 'Ram')].tolist()
    stock_names=[]
    for name in company_names:
        ticker=get_stock_name(name)
        stock_names.append(ticker)
        file_name=name.replace(" ","_")
        data = yf.download(ticker, start="2020-01-01", end="2024-11-29")
         # Xuất dữ liệu ra file Excel    
        folder_path = r"C:\Users\admin\Desktop\XLDL\Stock_data"
        file_path = os.path.join(folder_path, file_name + ".xlsx")
        data.to_excel(file_path, engine='openpyxl')
    return stock_names 
