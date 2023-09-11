from datetime import datetime, timedelta
from datetime import date
from shopeeAuth import ShopeeAffiliate, ATAffiliate
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
import random
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, ColumnsAutoSizeMode
import re
from urlextract import URLExtract
# import urlexpander
import pyshorteners
from pyshorteners import Shortener
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# from webdriver_manager.chrome import ChromeDriverManager
import pickle
from selenium.webdriver.common.keys import Keys
from time import sleep
from urllib.parse import unquote
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
import os
import streamlit as st
from streamlit_ace import st_ace, KEYBINDINGS, LANGUAGES, THEMES

os.environ['GH_TOKEN'] = "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"


st.set_page_config(
        page_title='Tạo Link Shopee Affiliate',
        page_icon="😍"                  
        )
    
# BACKGROUND_COLOR = 'white'
# COLOR = 'black' 


if 'driver' not in st.session_state:
    st.session_state.driver = None
if 'shopeeId' not in st.session_state:
    st.session_state.shopeeId = ''

currentShopee = ''


@st.cache_resource
def installff():
  os.system('sbase install geckodriver')
  os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver')

_ = installff()

@st.cache_resource
def openChrome():
    global driver
    options = Options()
    # options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    # options.add_argument("--user-data-dir=C:\\Users\\nguye\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 56")
    # options.add_experimental_option("detach", True)
    # if checkSystem == "Windows":
    #     drivePath = "./geckodriver.exe"
    # elif checkSystem == "MacOS":
    #     drivePath = "./geckodriver"
        
    driver = webdriver.Firefox(
        options=options,
        # service=Service(GeckoDriverManager().install()),
       
        
    )
    # driver.get("https://affiliate.shopee.vn/dashboard")
    
    if appid == "17318220053":
        username = "nguyenhoaibaoltt@gmail.com"
        password = "thaidunGG512976!"
        filename = "17318220053_my_cookie.pkl"
    if appid == "17380760085":
        username = "nguyenthithanhdungst@gmail.com"
        password = "Hoaibao232!"
        filename = "17380760085_my_cookie.pkl"
    if appid == "17328650055":
        username = "bichthu04@gmail.com"
        password = "Hoaivan74203(8&5"
        filename = "17328650055_my_cookie.pkl"
    if appid == "17344960081":
        username = "hoaibao2321999@gmail.com"
        password = "thaidunGG576!@"
        filename = "17344960081_my_cookie.pkl"

    driver.get("https://affiliate.shopee.vn/offer/custom_link")
    
    try:
        cookies = pickle.load(open(filename,"rb"))
        print("LOAD COOKIE")

        for cookie in cookies:
            driver.add_cookie(cookie)
    except:
        print("LOAD COOKIE FAIL")
    sleep(5)
    
   
    try:
        txtUser = driver.find_element(By.NAME,"loginKey")
        txtUser.send_keys(username)

        txtPassword = driver.find_element(By.NAME,"password")
        txtPassword.send_keys(password)

        txtPassword.send_keys(Keys.ENTER)

        sleep(10)

        pickle.dump(driver.get_cookies(), open(filename,"wb"))
        
        print("LOGIN DONE")

    except:
        print ("LOGGED")
        
    st.session_state.shopeeId = appid
        
    return driver

def shopeeCookieLink(driver,urls,utmContent2):
    # 3. Refresh the browser
    # driver.get("https://affiliate.shopee.vn/offer/custom_link")
    # sleep(10)
    
    try:
        txtUser1 = driver.find_element(By.NAME,"loginKey")
        print ("BI LOGOUT")
    except:
        print ("VAN CON LOG")
        
    try:
        buttonclose = driver.find_element(By.XPATH, "//button[@class='ant-btn']");
        buttonclose.click()
    except:
        print("1")
        
    sleep(2)

    link = urls
    shortenURL = ''

    # for link in linkArr:
    # print(link)
    try:
        txtLink = driver.find_element(By.XPATH, '//textarea[@class="ant-input"]');
        # txtLink.click()
        txtLink.clear()
        txtLink.send_keys(link)
    except:
        print("ERROR 1 ")
    
    try:
        subId1 = driver.find_element(By.ID, 'customLink_sub_id1');
        # subId1.click()
        subId1.clear()
        subId1.send_keys(utmContent2)
    except:
        print("ERROR 2")

    try:
        submitBtn = driver.find_element(By.XPATH, '//button[@type="submit"]');
        submitBtn.click()
        sleep(3)
        shortenLink = driver.find_elements(By.XPATH,'//textarea[@class="ant-input ant-input-disabled"]')
    except:
        print("ERROR 3")
        
    for i in shortenLink:
        shortenURL = i.text
        # print(shortenURL)
    
    if "\n" in shortenURL:
        shortenURL = shortenURL.split("\n")
    else:
        shortenURL = shortenURL.split()
    
    try:
        closeBtn = driver.find_element(By.XPATH, '/html/body/div[4]/div/div[2]/div/div[2]/button');
        closeBtn.click()
    except:
        closeBtn = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[2]/button');
        closeBtn.click()

    return shortenURL
        # driver.get("https://affiliate.shopee.vn/offer/custom_link")
        # sleep(5)

abc = st.expander("Kiểm tra tài khoản Shopee đang chạy tại đây")

colu1, colu2 = st.columns(2)
with colu1:
    taskPeople = st.selectbox(
        'Người làm',
        ['BAO', 'LUT', 'VAN', 'VI'])
with colu2:
    checkMGG = st.selectbox(
        'Mã giảm giá',
        ['', 'MGG'])
     
appid = "17318220053" # Your appid

coll1, coll2 = st.columns(2)
with coll1:
    appid = st.selectbox(
        'Tài khoản Shopee',
        ['17318220053', '17328650055', '17380760085','17344960081'])
    # appid = st.selectbox(
    #     'Tài khoản Shopee',
    #     ['17318220053'])
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
elif appid == "17344960081":
    secret = ""

if ATid == "1":
    accessKey = "rtFpJnRsPYs9A4edyv2UAHRQxP20Lq4A"
elif ATid == "2":
    accessKey = "GVR5cejXtxeUkDzlTsqH6aJOYx9yt1Ae"
elif ATid == "3":
    accessKey = "jZGjKwszHSHBmo-HAkq9NUmjxMJZ1mqf"


with abc:
    aaaa = st.success('Tài khoản Shopee bạn đang sử dụng để tạo link là {}'.format(st.session_state.shopeeId), icon="✅")
   
    
    collll1, collll2, cot3 = st.columns(3)   
    with collll1:
        checkBtn = st.button("Check") 
    with collll2:
        openBtn = st.button("Open FireFox")
    with cot3:
        closeBtn = st.button("Close FireFox")
            
    if openBtn:
        st.session_state.driver = openChrome()
    if closeBtn:
        driver = st.session_state.driver
        st.session_state.shopeeId = 'BROWSER ĐANG TẮT'
        st.cache_resource.clear()
        try:
            driver.quit()
        except:
            print("DRIVER QUIT ERROR")
  
    if checkBtn:
        print("CHECKED")
        

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
    number = st.number_input('Số link cần tạo:', step=1, max_value=5)
    df = pd.DataFrame(data,columns=['Sản phẩm', 'Category', 'Link gốc', 'Shopee Link', 'Comment', 'Note'])
    # df = df.rename(columns={'0': 'San Pham', '1': 'Category','2': 'Source Link','3': 'Aff Link'})

category = df['Category'].values
category=[*set(category)]

with colk1:
    option = st.selectbox(
        'Chọn loại sản phẩm',
        category)


with st.expander("Nhập văn bản cần tạo link"):  
    customLinks = st.text_area('Điền danh sách link hoặc cả đoạn text', '', key="text")

def clear_text():
    st.session_state["text"] = ""

df = df.loc[df['Category'] == option]


with st.expander("Affiliate trực tiếp với Shopee, làm mã giảm giá"): 
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        button1 = st.button('Tạo Link random')

    with col4:
        button2 = st.button('Custom Link 👌')
        
    with col3:
        buttonTiny = st.button('Rút gọn Link tiny')

    with col2:
        button3 = st.button('Tạo Link đã chọn')
    
    
with st.expander("Affiliate trung gian, dùng cho Shopee, Lazada, Tiki"): 
    col4, col5, col6 = st.columns(3)
    with col4:
        button4 = st.button('Tạo Link random AT')
        
    with col5:
        button5 = st.button('Tạo Link đã chọn AT')
        
    with col6:
        button6 = st.button('Custom Link AT')

c = st.container()

if button1:
    driver = openChrome()
    driver.get("https://affiliate.shopee.vn/offer/custom_link")
    texttt = st.empty()
    sa = ShopeeAffiliate(appid, secret)
    at = ATAffiliate(accessKey)
    df = df.loc[df['Category'] == option]
    df = df.sample(n = number)
    # randomeResult = random.sample(data, number)
    print(df)
    
    sourceLinks = df['Link gốc'].values
    affLinks = []
    
    todayDate = date.today()
    dt = datetime.now()
    ts = round(datetime.timestamp(dt))
    print(ts)
    utmContent1 = str(todayDate).replace("-", "") + str(ts)
    utmContent2 = taskPeople + utmContent1
    
    print(sourceLinks)
    output = "\n".join(sourceLinks)
    sleep(2)  
    res = shopeeCookieLink(driver,output,utmContent2)
    
    affLinks = affLinks + res
    print(affLinks)
        
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
    driver = openChrome()
    driver.get("https://affiliate.shopee.vn/offer/custom_link")
    
    texttt = st.empty()
    sa = ShopeeAffiliate(appid, secret)
    at = ATAffiliate(accessKey)
    for index, element in enumerate(data['selected_rows']):
        srcLink = data['selected_rows'][index]['Link gốc']
        cmtCapt = data['selected_rows'][index]['Comment']
        commentCaption.append(cmtCapt)
        selectedLinks.append(srcLink)
        
        
    todayDate = date.today()
    dt = datetime.now()
    ts = round(datetime.timestamp(dt))
    print(ts)
    utmContent1 = str(todayDate).replace("-", "") + str(ts)
    utmContent2 = taskPeople + utmContent1
    
    print(selectedLinks)
    output = "\n".join(selectedLinks)
    sleep(2)  
    res = shopeeCookieLink(driver,output,utmContent2)
    affLinks1 = affLinks1 + res
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

def find(URL):
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',URL) 
    return url

urls = []
lines = []
affLinks12 = []
if button6:
    xShort = Shortener()
    yShort = xShort.tinyurl
    sa = ShopeeAffiliate(appid, secret)
    at = ATAffiliate(accessKey)
    type_tiny = pyshorteners.Shortener()
    print(customLinks)
    
    extractor = URLExtract()
    lines = extractor.find_urls(customLinks)
    print(lines)
  
    # lines = customLinks.split("\n")
    # print(lines)
    affLinks11=[]
    str11=""
    campaign_id =""
    for k in lines:
        k = k.replace(",","")
        # k = urlexpander.expand(k)
        # print(k)
        if ("https://shopee.vn" in k) or ("https://lazada.vn" in k) or ("https://tiki.vn" in k):
            print("ok")
        else:   
            try:
                response = requests.head(k)
                print("++++++++++")
                print(response.headers['location'])
                k = response.headers['location']
            except:
                k = ""
                
            try:
                response = requests.head(k)
                print(response.headers['location'])
                k = response.headers['location']
            except:
                k = ""

        todayDate = date.today()
        dt = datetime.now()
        ts = round(datetime.timestamp(dt))
        print(ts)
        utmContent1 = str(todayDate).replace("-", "") + str(ts)
        if checkMGG == "MGG":
            utmContent2 = taskPeople + "MGG"
        else:
            utmContent2 = taskPeople
        print(utmContent1)
        print(utmContent2)
        if "lazada" in k:
            campaign_id = "5127144557053758578"
        elif "tiki" in k:
            campaign_id = "4348614231480407268"
        elif "shopee" in k:
            campaign_id = "4751584435713464237"
        elif "shope.ee" in k:
            campaign_id = "4751584435713464237"
        
        if k != "":
            try:
                res = at.generateShortLink(k, campaign_id, utmContent1, utmContent2, option)
            except:
                res = ""
            if checkMGG == "MGG":
                try:
                    res = type_tiny.tinyurl.short(res)
                except:
                    try:
                        res = yShort.short(k)
                    except:
                        res = res
            affLinks11.append(res)
        else:
            res = k
            affLinks11.append(res)
    
    affLinks12 = affLinks11
    
    for element in affLinks11:
        cmtContent = element + "\n"
        cmtContent = cmtContent.replace("\n","  \n")
        print (cmtContent)
        str11 = str11 + cmtContent
    

    for x, y in zip(lines, affLinks12):
        customLinks = customLinks.replace(x, y)

    print(customLinks)
    # aXbYcZd
    
    text_to_be_copied = str11
    # pyperclip.copy(text_to_be_copied)

    print (str11)
    with c:
        st.code(customLinks, language="csv", line_numbers=False)   
# st.dataframe(df, use_container_width=True)

middleURL = []

if button2:
    driver = openChrome()
    driver.get("https://affiliate.shopee.vn/offer/custom_link")
    sa = ShopeeAffiliate(appid, secret)
    at = ATAffiliate(accessKey)
    type_tiny = pyshorteners.Shortener()
    print(customLinks)
    
    extractor = URLExtract()
    lines = extractor.find_urls(customLinks)
    print(lines)
  
    # lines = customLinks.split("\n")
    # print(lines)
    affLinks11=[]
    str11=""
    campaign_id =""
    for k in lines:
        k = k.replace(",","")
        # k = urlexpander.expand(k)
        # print(k)
        try:
            response = requests.head(k)
            print(response.headers['location'])
            print('==============')
            k = response.headers['location']
        except:
            k = k
        
        if "https://shope.ee/an_redir?origin_link" in k:
            k = k.split('origin_link=')[1]
            k = unquote(k)
            # print(k)
            if "?utm" in k:
                k = k.split('?utm')[0]
            elif "&utm" in k:
                k = k.split('&utm')[0]
            print(k)
        else:
            try:
                response = requests.head(k)
                print(response.headers['location'])
                print('+++++++++++++++')
                k = response.headers['location']
                if "?utm" in k:
                    k = k.split('?utm')[0]
                elif "&utm" in k:
                    k = k.split('&utm')[0]
                print(k)
            except:
                print("ERROR ERROR")

        if not ("lazada.vn" in k or "shopee.vn" in k or "tiki.vn" in k):
            k = "https://shopee.vn"
        middleURL.append(k)

    for k in range(0, len(middleURL), 5):
        output = "\n".join(middleURL[k:k + 5])
        
        print(output)
        # todayDate = date.today()
        # dt = datetime.now()
        # ts = round(datetime.timestamp(dt))
        # # print(ts)
        # utmContent1 = str(todayDate).replace("-", "") + str(ts)
        if checkMGG == "MGG":
            utmContent2 = taskPeople + "MGG"
        else:
            utmContent2 = taskPeople
        # print(utmContent1)
        # print(utmContent2)
        # if "lazada" in k:
        #     campaign_id = "5127144557053758578"
        # elif "tiki" in k:
        #     campaign_id = "4348614231480407268"
        # elif "shopee" in k:
        #     campaign_id = "4751584435713464237"
        # elif "shope.ee" in k:
        #     campaign_id = "4751584435713464237"
        
        if middleURL[k] != "":
            try:
                if ("shopee.vn" in middleURL[k]):
                    sleep(2)
                    print("RUT GON LINK")
                    res = shopeeCookieLink(driver,output,utmContent2)
                    print(res)
                elif ("lazada.vn" in middleURL[k]):
                    try:
                        res = type_tiny.tinyurl.short(k)
                    except:
                        res = k
                elif ("tiki.vn" in middleURL[k]):
                    try:
                        res = at.generateShortLink(k, '4348614231480407268', utmContent1, utmContent2, option)
                    except:
                        res = k
                else:
                    res = [";"]
            except:
                print("Something else went wrong")
                res = []
            # if checkMGG == "MGG":
            #     try:
            #         res = type_tiny.tinyurl.short(res)
            #     except:
            #         res = res
            affLinks11 = affLinks11 + res
        else:
            res = middleURL[k].split()
            affLinks11 = affLinks11 + res
    
    affLinks12 = affLinks11
    
    for element in affLinks11:
        cmtContent = element + "\n"
        cmtContent = cmtContent.replace("\n","  \n")
        print (cmtContent)
        str11 = str11 + cmtContent
            
    for x, y in zip(lines, affLinks12):
        customLinks = customLinks.replace(x, y)

    print(customLinks)
    
    text_to_be_copied = str11
    # pyperclip.copy(text_to_be_copied)

    print (str11)
    with c:
        st.code(customLinks, language="csv", line_numbers=False)
        
    # driver.quit();   

if buttonTiny:
    xShort = Shortener()
    yShort = xShort.tinyurl
    type_tiny = pyshorteners.Shortener()
    extractor = URLExtract()
    lines = extractor.find_urls(customLinks)
    print(lines)
  
    # lines = customLinks.split("\n")
    # print(lines)
    affLinks11=[]
    str11=""
    campaign_id =""
        
    for k in lines:
        if k != "":
            try:
                res = type_tiny.tinyurl.short(res)
            except:
                try:
                    res = yShort.short(k)
                except:
                    print("Something else went wrong")
                    if "https://shorten.asia" in k:
                        res = k
                    else:
                        res = ""
        
            affLinks11.append(res)
        else:
            res = k
            affLinks11.append(res)
    
    affLinks12 = affLinks11
    
    print (affLinks11)
    
    for element in affLinks11:
        cmtContent = element + "\n"
        cmtContent = cmtContent.replace("\n","  \n")
        print (cmtContent)
        str11 = str11 + cmtContent
    

    for x, y in zip(lines, affLinks12):
        customLinks = customLinks.replace(x, y)

    print(customLinks)
    
    text_to_be_copied = str11
    # pyperclip.copy(text_to_be_copied)

    print (str11)
    with c:
        st.code(customLinks, language="csv", line_numbers=False)


# if button2:
#     sa = ShopeeAffiliate(appid, secret)
#     at = ATAffiliate(accessKey)
#     print(customLinks)
#     lines = customLinks.split("\n")
#     print(lines)
#     affLinks11=[]
#     str11=""
#     for k in lines:
#         print(k)
#         todayDate = date.today()
#         dt = datetime.now()
#         ts = round(datetime.timestamp(dt))
#         print(ts)
#         utmContent1 = str(todayDate).replace("-", "") + str(ts)
#         utmContent2 = taskPeople
#         print(utmContent1)
#         print(utmContent2)
#         if "lazada" in k:
#             campaign_id = "5127144557053758578"
#             res = at.generateShortLink(k, campaign_id, utmContent1, utmContent2, option)
#         elif "tiki" in k:
#             campaign_id = "4348614231480407268"
#             res = at.generateShortLink(k, campaign_id, utmContent1, utmContent2, option)
#         elif "shopee" in k:
#             res = sa.generateShortLink(k, utmContent1, utmContent2, option)
#         print(res)
#         affLinks11.append(res)
 
#     for element in affLinks11:
#         cmtContent = element + "\n"
#         cmtContent = cmtContent.replace("\n","  \n")
#         print (cmtContent)
#         str11 = str11 + cmtContent
    
#     text_to_be_copied = str11
#     # pyperclip.copy(text_to_be_copied)

#     print (str11)
#     st.code(str11, language="csv", line_numbers=False)


st.header("Dùng để chỉnh sửa text")
content = st_ace(
    language='plain_text', theme='chrome',
    key="ace",
    font_size=14, tab_size=6,
)

if content:
    st.subheader("Content")
    st.code(content,language='plain_text')