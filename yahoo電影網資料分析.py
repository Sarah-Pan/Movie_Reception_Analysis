# -*- coding: utf-8 -*-
"""Yahoo電影網資料分析.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_J7LXUOaS3-Aj-dmhpYwDc3zcv4yvjq2

主題：透過爬取Yahoo電影網上映中院線電影的資料判斷觀影者的期待度(Anticipation)是否與滿意度(Satisfaction)相關
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

res = requests.get("https://movies.yahoo.com.tw/movie_intheaters.html?page=1")
soup = BeautifulSoup(res.text,"html.parser")

"""爬取電影名稱、期待度與滿意度，由於有些電影沒有釋出滿意度或期待度，因此我一次爬取三種資料輸出成表格，以便辨識缺失值的位置。"""

url = "https://movies.yahoo.com.tw/movie_intheaters.html?page=1"
Big_list = []
for i in range(8):   
  res = requests.get(url)
  soup = BeautifulSoup(res.text,"html.parser")
  titles = soup.select('div.release_movie_name,a.release_movie_name')
  Big_list.append(titles)
  if i == 7:
    break
  paging = soup.select('.nexttxt a')
  next_url = paging[0]["href"]
  url = next_url

Big_list_text = []

for titles in Big_list:
  for t in range(len(titles)):
    print(titles[t].text)
    Big_list_text.append(titles[t].text)

clean = []
for data in Big_list_text:
 clean.append(data.split('\n'))

num = 0
for titles in Big_list:
  len(titles)
  num += len(titles)
num

"""將爬取好的資料輸出成Excel表格"""

df = pd.DataFrame(clean)
#print(df)
df.to_excel("clean.xlsx")

"""此時發現滿意度(Satisfaction)數值藏在HTML標籤中的屬性"Data-num"中，而不是標籤的文字內容，無法像電影名稱以及期待度(Anticipation)一樣直接爬取。
因此我再設定一次爬蟲爬取data-num屬性中的數值。
"""

url = "https://movies.yahoo.com.tw/movie_intheaters.html?page=1"
sat_list = []
for i in range(8):
  res = requests.get(url)
  soup = BeautifulSoup(res.text,"html.parser")
  span_tag = soup.select('.levelbox dd span')
  data_num = [] 
  for data in span_tag:
    dn = data.get("data-num")
    data_num.append(dn)
  sat_list.append(data_num)
  if i == 7:
    break
  paging = soup.select('.nexttxt a')
  next_url = paging[0]["href"]
  url = next_url

sat_list

"""爬取後將其下載成Excel表格"""

df = pd.DataFrame(sat_list)
#print(df)
df.to_excel("sat_list.xlsx")

"""接下來使用Excel將資料缺失值以NAN填補，並將滿意度(Satisfaction)數據與原表格合併

將合併過後的表格以pandas讀取成DataFrame
"""

from google.colab import drive
drive.mount('/content/drive')

df = pd.read_csv('/content/drive/MyDrive/movie_analysis.csv',encoding='big5')

df

df.drop('Unnamed: 4',inplace = True, axis=1)
df

df.rename(columns = {'期待度':'Anticipation','滿意度':'Satisfaction'}, inplace = True)
df

"""做出散佈圖以判斷電影的期待度(Anticipation)是否與滿意度(Satisfaction)有相關"""

g = sns.scatterplot(x='Anticipation',y='Satisfaction',data = df).invert_yaxis()
plt.title("Correlation between Anticipation and Satisfaction.")

"""結論:由右上角多點向上可判讀滿意度和期待度呈現正相關"""