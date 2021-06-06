import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import urllib
import csv
from bs4 import BeautifulSoup
import re
from urllib.request import Request, urlopen
from PIL import Image
import time



st.set_page_config(layout="wide")
image = Image.open('house.png')
st.image(image, width = 500)
st.title('HDB Resale Flats Dashboard')

st.markdown("""
**This app retrieves data of HDB Resale Prices from data.gov.sg.**
""")

st.sidebar.header('User Input Features')

# Web scraping of data.gov.sg data
#
@st.cache
def load_data():
    myDataFrame = pd.DataFrame()
    #Live Extraction from data.gov.sg
    #urldata = ['https://storage.data.gov.sg/resale-flat-prices/resources/resale-flat-prices-based-on-registration-date-from-jan-2017-onwards-2021-06-04T02-52-32Z.csv']
    #, 'https://storage.data.gov.sg/resale-flat-prices/resources/resale-flat-prices-based-on-registration-date-from-jan-2015-to-dec-2016-2019-06-17T09-03-16Z.csv', \
    #       'https://storage.data.gov.sg/resale-flat-prices/resources/resale-flat-prices-based-on-registration-date-from-mar-2012-to-dec-2014-2019-06-17T09-04-34Z.csv', \
    #       'https://storage.data.gov.sg/resale-flat-prices/resources/resale-flat-prices-based-on-approval-date-2000-feb-2012-2019-06-28T10-14-13Z.csv', \
    #       'https://storage.data.gov.sg/resale-flat-prices/resources/resale-flat-prices-based-on-approval-date-1990-1999-2021-05-25T02-49-29Z.csv']
    #for links in urldata:
    #    req = Request(links)
    #    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0')
    #    content = urlopen(req)
    #    df = pd.read_csv(content)
    #    myDataFrame = myDataFrame.append(df)
    #    myDataFrame.sort_values(by = ['month'],ascending = False)
    #Saved in Github
    df = pd.read_csv('resale-flat-prices-based-on-registration-date-from-jan-2017-onwards.csv')
    myDataFrame = myDataFrame.append(df)
    myDataFrame.sort_values(by = ['month'],ascending = False)
    return myDataFrame
df = load_data()

    
town = df.groupby('town')
#subsector = df.groupby('GICS Sub-Industry')

# Sidebar - Sector selection
sorted_town_unique = sorted( df['town'].unique() )
selected_town = st.sidebar.multiselect('Town', sorted_town_unique, sorted_town_unique) #Label, Options, Default list of values = none


# Filtering data
df_selected_town = df[ (df['town'].isin(selected_town)) ]


st.header('Display Resale Flats in Selected Towns')
st.write('All filters are offed initially')
st.write('Data Dimensions: ' + str(df_selected_town.shape[0]) + ' rows and ' + str(df_selected_town.shape[1]) + ' columns.')
st.dataframe(df_selected_town)



def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="Resale_prices.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_town), unsafe_allow_html=True)



# Plot Price of Resale Price
def price_plot(town):
#  df = pd.DataFrame(data[symbol].Close)
#  df['Date'] = df.index
  fig,ax = plt.subplots()
  plt.fill_between(df_selected_town.month, df_selected_town.resale_price, color='skyblue', alpha=0.3)
  plt.plot(df_selected_town.month, df_selected_town.resale_price, color='skyblue', alpha=0.8)
  plt.xticks(rotation=90)
  plt.title(town, fontweight='bold')
  plt.xlabel('Month', fontweight='bold')
  plt.ylabel('Price', fontweight='bold')
  return st.pyplot(fig)

num_town = st.sidebar.slider('Number of Towns', 1, 10)


#st.header('Stock Closing Price')
for i in list(df_selected_town.town)[:num_town]:
    price_plot(i)

