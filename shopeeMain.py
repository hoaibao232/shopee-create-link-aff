from datetime import datetime, timedelta
from datetime import date
from shopeeAuth import ShopeeAffiliate, ATAffiliate
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
import random
import numpy as np
import pyperclip
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, ColumnsAutoSizeMode


st.set_page_config(
        page_title='Tạo Link Shopee Affiliate',
        page_icon="😍"                  
        )

BACKGROUND_COLOR = 'white'
COLOR = 'black'

with st.expander("Thông báo"):
    st.success("Hiện tại Shopee đang bị lỗi tạo link, nên mọi người tạm thời sử dụng các tính năng trong phần 'Tạo Link AT' nhé. Tool đã có thể tạo link cho 3 sàn Shopee, Lazada, Tiki")
    
taskPeople = st.selectbox(
    'Người làm',
    ['BAO', 'LUT', 'VAN', 'VI'])

appid = "17318220053" # Your appid

coll1, coll2 = st.columns(2)
with coll1:
    # appid = st.selectbox(
    #     'Tài khoản Shopee',
    #     ['17318220053', '17328650055', '17380760085'])
    appid = st.selectbox(
        'Tài khoản Shopee',
        ['17318220053'])
with coll2:
    ATid = st.selectbox(
        'Tài khoản AT',
        ['1', '2', '3'])

if appid == "17318220053":
    secret = "VQQEHZVTZS5ETDUI2KFHSFPW6YTCBCES"
elif appid == "17328650055":
    secret = "6AKO5VRGDUWBPDP5EIG7PP4E6W5VOBJL"
elif appid == "17380760085":
    secret = "F6QVZQDUBMOI57X74Q55U5U2EJ7HYPG3"

if ATid == "1":
    accessKey = "rtFpJnRsPYs9A4edyv2UAHRQxP20Lq4A"
elif ATid == "2":
    accessKey = "GVR5cejXtxeUkDzlTsqH6aJOYx9yt1Ae"
elif ATid == "3":
    accessKey = "jZGjKwszHSHBmo-HAkq9NUmjxMJZ1mqf"


data = []
selectedLinks = []
# report yesterday
startdate = datetime.now() - timedelta(days=5)
enddate = datetime.now() - timedelta(days=2)

# Khai báo client ID và client secret key
creds = service_account.Credentials.from_service_account_file(
    'shopee-a-5c7a7ee72e9c.json')

# Xác thực và đăng nhập vào tài khoản Google
service = build('sheets', 'v4', credentials=creds)

# Truy cập vào một bảng tính cụ thể
spreadsheet_id = '10eXnT79-Ng2SaP3lgASSiMv_w6F7WqjCa28178Kv5aY'
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

colk1, colk2 = st.columns(2)
with colk2:
    number = st.number_input('Số link cần tạo:', step=1)
    df = pd.DataFrame(data,columns=['Sản phẩm', 'Category', 'Link gốc', 'Shopee Link', 'Comment', 'Note'])
    # df = df.rename(columns={'0': 'San Pham', '1': 'Category','2': 'Source Link','3': 'Aff Link'})

category = df['Category'].values
category=[*set(category)]

with colk1:
    option = st.selectbox(
        'Chọn loại sản phẩm',
        category)


with st.expander("Custom Link"):  
    customLinks = st.text_area('Điền danh sách link', '', key="text")

def clear_text():
    st.session_state["text"] = ""

df = df.loc[df['Category'] == option]


with st.expander("Tạo Link Shopee"): 
    col1, col2, col3 = st.columns(3)
    with col1:
        button1 = st.button('Tạo Link random', on_click=clear_text)

    with col3:
        button2 = st.button('Custom Link')

    with col2:
        button3 = st.button('Tạo Link đã chọn', on_click=clear_text)
    
    
with st.expander("Tạo Link AT"): 
    col4, col5, col6 = st.columns(3)
    with col4:
        button4 = st.button('Tạo Link random AT', on_click=clear_text)
        
    with col5:
        button5 = st.button('Tạo Link đã chọn AT', on_click=clear_text)
        
    with col6:
        button6 = st.button('Custom Link AT')

c = st.container()

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
        utmContent1 = str(todayDate).replace("-", "") + str(ts)
        utmContent2 = taskPeople
        print(utmContent1)
        print(utmContent2)
        if "lazada" in x:
            res = ""
        else:
            res = sa.generateShortLink(x, utmContent1, utmContent2, option)
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

if button4:
    texttt = st.empty()
    at = ATAffiliate(accessKey)
    
    texttt = st.empty()
    at = ATAffiliate(accessKey)
    df = df.loc[df['Category'] == option]
    df = df.sample(n = number)
    print(df)
    
    sourceLinks = df['Link gốc'].values
    affLinks = []
    campaign_id = ""
    for x in sourceLinks:
        print(x)
        todayDate = date.today()
        dt = datetime.now()
        ts = round(datetime.timestamp(dt))
        print(ts)
        utmContent1 = str(todayDate).replace("-", "") + str(ts)
        utmContent2 = taskPeople
        print(utmContent1)
        print(utmContent2)
        if "lazada" in x:
            campaign_id = "5127144557053758578"
        elif "shopee" in x:
            campaign_id = "4751584435713464237"
        elif "tiki" in x:
            campaign_id = "4348614231480407268"
        res = at.generateShortLink(x, campaign_id, utmContent1, utmContent2, option)
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
    at = ATAffiliate(accessKey)
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
        utmContent1 = str(todayDate).replace("-", "") + str(ts)
        utmContent2 = taskPeople
        print(utmContent1)
        print(utmContent2)
        if "lazada" in k:
            campaign_id = "5127144557053758578"
            res = at.generateShortLink(k, campaign_id, utmContent1, utmContent2, option)
        elif "tiki" in k:
            campaign_id = "4348614231480407268"
            res = at.generateShortLink(k, campaign_id, utmContent1, utmContent2, option)
        elif "shopee" in k:
            res = sa.generateShortLink(k, utmContent1, utmContent2, option)
        print(res)
        affLinks11.append(res)
 
    for element in affLinks11:
        cmtContent = element + "\n"
        cmtContent = cmtContent.replace("\n","  \n")
        print (cmtContent)
        str11 = str11 + cmtContent
    
    text_to_be_copied = str11
    # pyperclip.copy(text_to_be_copied)

    print (str11)
    st.code(str11, language="csv", line_numbers=False)

    
# select the columns you want the users to see
gb = GridOptionsBuilder.from_dataframe(df)
# configure selection
gb.configure_selection(selection_mode="multiple", use_checkbox=True)
gb.configure_side_bar()
gridOptions = gb.build()

data = AgGrid(df,
              gridOptions=gridOptions,
              enable_enterprise_modules=True,
              allow_unsafe_jscode=True,
              update_mode=GridUpdateMode.SELECTION_CHANGED,
              columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS)

affLinks1 = []
commentCaption =[]
str11 = ""
if button3:
    texttt = st.empty()
    sa = ShopeeAffiliate(appid, secret)
    at = ATAffiliate(accessKey)
    for index, element in enumerate(data['selected_rows']):
        srcLink = data['selected_rows'][index]['Link gốc']
        cmtCapt = data['selected_rows'][index]['Comment']
        commentCaption.append(cmtCapt)
        selectedLinks.append(srcLink)

    for x in selectedLinks:
        print(x)
        todayDate = date.today()
        dt = datetime.now()
        ts = round(datetime.timestamp(dt))
        print(ts)
        utmContent1 = str(todayDate).replace("-", "") + str(ts)
        utmContent2 = taskPeople
        print(utmContent1)
        print(utmContent2)
        
        if "lazada" in x:
            campaign_id = "5127144557053758578"
            res = at.generateShortLink(x, campaign_id, utmContent1, utmContent2, option)
        elif "tiki" in x:
            campaign_id = "4348614231480407268"
            res = at.generateShortLink(x, campaign_id, utmContent1, utmContent2, option)
        elif "shopee" in x:
            res = sa.generateShortLink(x, utmContent1, utmContent2, option)
        print(res)
        affLinks1.append(res)
        

    print(affLinks1)
    # print(df)
        
    # for i, prod in enumerate(df.index):
    #     df.iloc[i, 3] = affLinks1[i]
        
    for i in range(len(affLinks1)):
        cmtContent = commentCaption[i] + affLinks1[i] + "\n\n"
        cmtContent = cmtContent.replace("\n","  \n")
        print (cmtContent)
        str11 = str11 + cmtContent

    print (str11)
    with c:
        st.code(str11, language="csv", line_numbers=False)

if button5:
    texttt = st.empty()
    sa = ShopeeAffiliate(appid, secret)
    at = ATAffiliate(accessKey)
    for index, element in enumerate(data['selected_rows']):
        srcLink = data['selected_rows'][index]['Link gốc']
        cmtCapt = data['selected_rows'][index]['Comment']
        commentCaption.append(cmtCapt)
        selectedLinks.append(srcLink)

    for x in selectedLinks:
        print(x)
        todayDate = date.today()
        dt = datetime.now()
        ts = round(datetime.timestamp(dt))
        print(ts)
        utmContent1 = str(todayDate).replace("-", "") + str(ts)
        utmContent2 = taskPeople
        print(utmContent1)
        print(utmContent2)
        
        if "lazada" in x:
            campaign_id = "5127144557053758578"
        elif "tiki" in x:
            campaign_id = "4348614231480407268"
        elif "shopee" in x:
            campaign_id = "4751584435713464237"    
        res = at.generateShortLink(x, campaign_id, utmContent1, utmContent2, option)
        affLinks1.append(res)
        

    print(affLinks1)
    # print(df)
        
    # for i, prod in enumerate(df.index):
    #     df.iloc[i, 3] = affLinks1[i]
        
    for i in range(len(affLinks1)):
        cmtContent = commentCaption[i] + affLinks1[i] + "\n\n"
        cmtContent = cmtContent.replace("\n","  \n")
        print (cmtContent)
        str11 = str11 + cmtContent

    print (str11)
    with c:
        st.code(str11, language="csv", line_numbers=False)

if button6:
    sa = ShopeeAffiliate(appid, secret)
    at = ATAffiliate(accessKey)
    print(customLinks)
    lines = customLinks.split("\n")
    print(lines)
    affLinks11=[]
    str11=""
    campaign_id =""
    for k in lines:
        print(k)
        todayDate = date.today()
        dt = datetime.now()
        ts = round(datetime.timestamp(dt))
        print(ts)
        utmContent1 = str(todayDate).replace("-", "") + str(ts)
        utmContent2 = taskPeople
        print(utmContent1)
        print(utmContent2)
        if "lazada" in k:
            campaign_id = "5127144557053758578"
        elif "tiki" in k:
            campaign_id = "4348614231480407268"
        elif "shopee" in k:
            campaign_id = "4751584435713464237"  
        res = at.generateShortLink(k, campaign_id, utmContent1, utmContent2, option)
        affLinks11.append(res)
 
    for element in affLinks11:
        cmtContent = element + "\n"
        cmtContent = cmtContent.replace("\n","  \n")
        print (cmtContent)
        str11 = str11 + cmtContent
    
    text_to_be_copied = str11
    # pyperclip.copy(text_to_be_copied)

    print (str11)
    with c:
        st.code(str11, language="csv", line_numbers=False)   
# st.dataframe(df, use_container_width=True)