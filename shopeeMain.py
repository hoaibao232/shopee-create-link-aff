from datetime import datetime, timedelta
from datetime import date
from shopeeAuth import ShopeeAffiliate
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
import random
import numpy as np
import pyperclip



appid = "17318220053" # Your appid
secret = "VQQEHZVTZS5ETDUI2KFHSFPW6YTCBCES" # Your secret

st.set_page_config(
        page_title='Tạo Link Shopee Affiliate',
        page_icon="😍"                  
        )

data = []
# report yesterday
startdate = datetime.now() - timedelta(days=5)
enddate = datetime.now() - timedelta(days=2)

# Khai báo client ID và client secret key
creds = service_account.Credentials.from_service_account_file(
    'shopee-a-5c7a7ee72e9c.json')

# Xác thực và đăng nhập vào tài khoản Google
service = build('sheets', 'v4', credentials=creds)

# Truy cập vào một bảng tính cụ thể
spreadsheet_id = '1MaESBny44SzKehhytEcs8w4OUEPPYct5eNZWX8J27Fk'
sheet_name = 'Quản lý Link'
# range_name = f'{sheet_name}!A1:B5'
range_name = 'Quản lý Link'

# Lấy dữ liệu từ bảng tính
result = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id, range=range_name).execute()

# In ra các giá trị trong bảng tính
for row in result.get('values', []):
    data.append(row)

data = data[1:]

# sa1 = ShopeeAffiliate(appid, secret)
# res1 = sa1.report(startdate, enddate)
# conversion, estimation, startdate_, enddate_ = res1
# st.write("Doanh thu uoc tinh:", estimation)

# res = sa.generateShortLink("https://shopee.vn/shop/114077203", "BAO", "BIDA")
# print (res)
number = st.number_input('Số link cần tạo:', step=1)
df = pd.DataFrame(data,columns=['Sản phẩm', 'Category', 'Link gốc', 'Shopee Link', 'Comment', 'Note'])
# df = df.rename(columns={'0': 'San Pham', '1': 'Category','2': 'Source Link','3': 'Aff Link'})

# print (df)
category = df['Category'].values
category=[*set(category)]
# print(category)

option = st.selectbox(
    'Chọn loại sản phẩm',
    category)

taskPeople = st.selectbox(
    'Người làm',
    ['BAO', 'LUT', 'VAN'])

customLinks = st.text_area('Custom Link', '', key="text")

def clear_text():
    st.session_state["text"] = ""

df = df.loc[df['Category'] == option]

col1, col2, col3,col4,col5 = st.columns(5)

with col1:
    button1 = st.button('Tạo', on_click=clear_text)

with col5:
    button2 = st.button('Custom Link')

if button1:
    texttt = st.empty()
    sa = ShopeeAffiliate(appid, secret)
    df = df.loc[df['Category'] == option]
    df = df.sample(n = number)
    # randomeResult = random.sample(data, number)
    print(df)
    
    sourceLinks = df['Link gốc'].values
    affLinks = []
    for x in sourceLinks:
        print(x)
        todayDate = date.today()
        dt = datetime.now()
        ts = round(datetime.timestamp(dt))
        print(ts)
        utmContent = str(todayDate).replace("-", "") + taskPeople + str(ts)
        print(utmContent)
        if "lazada" in x:
            res = "Hãy gửi link Shopee thay vì Lazada"
        else:
            res = sa.generateShortLink(x, utmContent, option)
        print(res)
        affLinks.append(res)
        
    for i, prod in enumerate(df.index):
        df.iloc[i, 3] = affLinks[i]
        
    arrayData = np.array(df[['Shopee Link','Comment']])
    print(arrayData)
    str1=""
    for element in arrayData:
        cmtContent = element[1] + element[0] + "\n\n"
        cmtContent = cmtContent.replace("\n","  \n")
        print (cmtContent)
        str1 = str1 + cmtContent
    
    text_to_be_copied = str1
    # pyperclip.copy(text_to_be_copied)

    print (str1)
    # st.write(str1)
    st.code(str1, language="csv", line_numbers=False)



if button2:
    sa = ShopeeAffiliate(appid, secret)
    print(customLinks)
    lines = customLinks.split("\n")
    print(lines)
    affLinks11=[]
    str11=""
    for k in lines:
        print(k)
        todayDate = date.today()
        dt = datetime.now()
        ts = round(datetime.timestamp(dt))
        print(ts)
        utmContent = str(todayDate).replace("-", "") + taskPeople + str(ts)
        print(utmContent)
        res = sa.generateShortLink(k, utmContent, option)
        print(res)
        affLinks11.append(res)
 
    for element in affLinks11:
        cmtContent = element + "\n"
        cmtContent = cmtContent.replace("\n","  \n")
        print (cmtContent)
        str11 = str11 + cmtContent
    
    text_to_be_copied = str11
    pyperclip.copy(text_to_be_copied)

    print (str11)
    st.write(str11)

st.dataframe(df, use_container_width=True)