#!/usr/bin/env python
# coding: utf-8

# In[2]:


# upload required liberaries

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg
import seaborn as sns
import re
import urllib.request



# prepare streamlit page title
st.set_page_config(page_title='Veefriends NFT Dashboard', page_icon= ':bar_chart:', layout = 'wide')
# prepare streamlit page setup
header = st.container()

# Introduction on NFT
with header:
    st.title('Veefriends NFT Dashboard :bar_chart:')
    
    
# read the data
nft = pd.read_csv('veefriends.csv')
nft['date'] = pd.to_datetime(nft['date'])
nft_sales = nft[nft.type == 'sales']
nft_sales.rarity_attribute.fillna('Core', inplace =True, axis=0) 
no_zero_sales = nft_sales[nft_sales.sale_price_eth != 0]

    

st.sidebar.header('Select your NFT Data')
    
group = st.sidebar.multiselect('Group selection', 
                                   options = nft_sales['group_attribute'].unique(),
                                   default = nft_sales['group_attribute'].unique())

rarity = st.sidebar.multiselect('Rarity Selection', 
                                   options = nft_sales['rarity_attribute'].unique(),
                                   default = nft_sales['rarity_attribute'].unique())

# query df to enable filtering 
nft_selection = nft_sales.query(
    "group_attribute == @group & rarity_attribute == @rarity")


# prepare required metrics
total_sales = round(nft_selection.sale_price_eth.sum(), 2)
highest_sale = round(((nft_sales[nft_sales.sale_price_eth == nft_selection.sale_price_eth.max()]).sale_price_eth).values[0], 3)
lowest_sale = round(((no_zero_sales[no_zero_sales.sale_price_eth == no_zero_sales.sale_price_eth.min()]).sale_price_eth).values[0], 13)

# prepare colulmns
left_col, mid1_col,mid2_col,mid3_col, right_col = st.columns([2,1.7,0.9,1.7,0.9])

with left_col:
    st.subheader('Total Sales')
    st.subheader(f'ETH {total_sales:,}')
    
with mid1_col:
    st.subheader('Highest Sale')
    st.subheader(f'ETH {highest_sale:,}')
    
    
with mid2_col:
    st.image('https://lh3.googleusercontent.com/pjja9yQOgIzrAfFPwgXi-KfQTz-Kxw-jZkDGoA0XGfYJc1325nQ9vc5xi1-eyFtM0lIETWInSGagyOAXsw2DqAIK1IE15jWeE_2U=w361',width=60)


with mid3_col:
    st.subheader('Lowest Sale')
    st.subheader(f'ETH {lowest_sale}')
    

with right_col:
    st.image('https://lh3.googleusercontent.com/Qsqx0ctFUoIGRH79I7hZV4wkvzNNcVnRapb0H2HrIeHAx5_RkF5H98biyrYq69t1svK3DffSg6sDcDTOuuPMZ8QZBxU3lWKSmdwSwA=w361',width=65)
    


# line chart 2
# prepare to plot relation between NFT groups and average price change
gift_sales = nft_selection[nft_selection.group_attribute == 'Gift']
access_sales = nft_selection[nft_selection.group_attribute == 'Access']
admission_sales = nft_selection[nft_selection.group_attribute == 'Admission']
gift = gift_sales.groupby("date").sale_price_eth.mean()
access = access_sales.groupby("date").sale_price_eth.mean()
admission = admission_sales.groupby("date").sale_price_eth.mean()
fig1, ax1 = plt.subplots(figsize = (12,4))
ax1.plot(gift)
ax1.plot(access)
ax1.plot(admission)
plt.title('NFT group price change over time')
plt.legend(['gift','access','asmission'])
plt.ylabel('Price in ETH')
st.pyplot(fig1);




# bar chart
cat = nft_selection.category_attribute.value_counts().index.to_list()
cat_color = ['navy', 'grey', 'maroon', 'green', 'darkorange', 'blue', 'brown', 'yellow', 'red', 'black']
fig, ax = plt.subplots(figsize = (11, 4))
ax = plt.barh(y = cat, width=nft_selection.category_attribute.value_counts().values, color = cat_color)
plt.title ('Veefriends NFT Categories')
plt.ylabel('Number of NFT')
plt.xlabel('Category Type')
st.pyplot(fig)







