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
import dask.dataframe as dd
from PIL import Image
import time

#---------------------------------#
# Page layout
## Page expands to full width
st.set_page_config(layout="wide")

#---------------------------------#
# Title

image = Image.open('house.png')

st.image(image, width = 500)
st.title('HDB Resale Flat Dashboard')

st.markdown("""
**This app retrieves data of HDB Resale Prices from data.gov.sg.**
""")

st.sidebar.header('User Input Features')

# Web scraping of data.gov.sg data
#
@st.cache(persist=True,show_spinner = True)
def load_data():
    myDataFrame = pd.DataFrame()
#    urldata = ['https://storage.data.gov.sg/resale-flat-prices/resources/resale-flat-prices-based-on-registration-date-from-jan-2017-onwards-2021-06-04T02-52-32Z.csv']
    #, 'https://storage.data.gov.sg/resale-flat-prices/resources/resale-flat-prices-based-on-registration-date-from-jan-2015-to-dec-2016-2019-06-17T09-03-16Z.csv', \
    #       'https://storage.data.gov.sg/resale-flat-prices/resources/resale-flat-prices-based-on-registration-date-from-mar-2012-to-dec-2014-2019-06-17T09-04-34Z.csv', \
    #       'https://storage.data.gov.sg/resale-flat-prices/resources/resale-flat-prices-based-on-approval-date-2000-feb-2012-2019-06-28T10-14-13Z.csv', \
    #       'https://storage.data.gov.sg/resale-flat-prices/resources/resale-flat-prices-based-on-approval-date-1990-1999-2021-05-25T02-49-29Z.csv']
#    for links in urldata:
#        req = Request(links)
#        req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0')
#        content = urlopen(req)
    df = pd.read_csv('resale-flat-prices-based-on-registration-date-from-jan-2017-onwards.csv')
    myDataFrame = myDataFrame.append(df)
    myDataFrame.sort_values(by = ['month'],ascending = False)
    return myDataFrame

myDataFrame = load_data()
town = myDataFrame.groupby('town')
#subsector = df.groupby('GICS Sub-Industry')

# Sidebar - Sector selection
#Filter by Town
sorted_town_unique = sorted( myDataFrame['town'].unique() )
selected_town = st.sidebar.multiselect('Town', sorted_town_unique,sorted_town_unique[0])
df_selected_town = myDataFrame[ (myDataFrame['town'].isin(selected_town)) ] #filtering data
#Filter by Flat Type
sorted_flattype_unique = sorted( df_selected_town['flat_type'].unique() )
selected_flattype = st.sidebar.multiselect('Flat Type', sorted_flattype_unique,sorted_flattype_unique)
df_town_flattype = df_selected_town[ (df_selected_town['flat_type'].isin(selected_flattype)) ] #filtering data

df_avgpriceoftown = myDataFrame.groupby('town').mean()

st.header('Average Prices among Towns')
st.write('Data Dimension: ' + str(df_avgpriceoftown.shape[0]) + ' rows and ' + str(df_avgpriceoftown.shape[1]) + ' columns.')
st.dataframe(df_avgpriceoftown)
fig,ax = plt.subplots()
st.bar_chart(df_avgpriceoftown.resale_price)


st.header('Display Resale Flats in Selected Town')
st.write('Data Dimension: ' + str(df_selected_town.shape[0]) + ' rows and ' + str(df_selected_town.shape[1]) + ' columns.')
st.dataframe(df_town_flattype)


# Download data
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="Resale_prices.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_town_flattype), unsafe_allow_html=True)

num_town = st.sidebar.slider('Number of Towns', 1, 10)

# Plot Price of Resale Price
def price_plot(town):
#  df = pd.DataFrame(data[symbol].Close)
#  df['Date'] = df.index
  fig,ax = plt.subplots()
  plt.fill_between(df_town_flattype.month[:1000], df_town_flattype.resale_price[:1000], color='darkcyan', alpha=0.3)
  plt.plot(df_town_flattype.month[:1000], df_town_flattype.resale_price[:1000], color='black', alpha=0.8)
  plt.xticks(rotation=90)
  plt.title('Price Behaviour for ' +  town, fontweight='bold')
  plt.xlabel('Month', fontweight='bold')
  plt.ylabel('Price', fontweight='bold')
  return st.pyplot(fig)


def price_plot1(town):
#  df = pd.DataFrame(data[symbol].Close)
#  df['Date'] = df.index
  COLOR = 'white'
  plt.rcParams['text.color'] = COLOR
  plt.rcParams['axes.labelcolor'] = COLOR
  plt.rcParams['axes.edgecolor'] = 'white'
  plt.rcParams['xtick.color'] = COLOR
  plt.rcParams['ytick.color'] = COLOR
  fig,ax = plt.subplots()
  ax.set_facecolor('xkcd:black')
  fig.set_facecolor('black')
  plt.hist(df_town_flattype.flat_type,bins = np.arange(5)-0.5, edgecolor = 'white', color='darkcyan', alpha=0.8)
  plt.xticks(rotation=90)
  plt.title('Dataset\'s Volume Breakdown of Flat Types for ' +  town, fontweight='bold')
  plt.xlabel('Flat Type', fontweight='bold')
  plt.ylabel('Count', fontweight='bold')
  return st.pyplot(fig)

#st.header('Stock Closing Price')
for i in list(selected_town)[:num_town]:
    price_plot1(i)
