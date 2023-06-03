import json
import requests as req
import pandas as pd
from bs4 import BeautifulSoup as bs
from urllib.parse import urlencode
from selenium import webdriver
import selenium.webdriver.common.by as By
import selenium.webdriver.common.keys as Keys
import undetected_chromedriver as uc
import requests
import gradio


class product:
    def __init__(self, name, price, location):
        self.name = name
        self.price = price
        self.location = location
#GET WEB INFO

def make_call(search):
    ac="text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    target_url= 'https://www.walmart.com/search?q='+ search +'&facet=fulfillment_method_in_store%3AIn-store'
    headers={"Referer":"https://www.google.com","Connection":"Keep-Alive","Accept-Language":"en-US,en;q=0.9","Accept-Encoding":"gzip, deflate, br","Accept":ac,"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
    
    resp = requests.get(target_url, headers=headers)
    soup = bs(resp.content, 'html.parser')
    return soup


# search = 'great+value+white+bread'

# ac="text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
# target_url= 'https://www.walmart.com/search?q='+ search +'&facet=fulfillment_method_in_store%3AIn-store'
# headers={"Referer":"https://www.google.com","Connection":"Keep-Alive","Accept-Language":"en-US,en;q=0.9","Accept-Encoding":"gzip, deflate, br","Accept":ac,"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
    
# resp = requests.get(target_url, headers=headers)
# soup = bs(resp.content, 'html.parser')

# script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
# json_blob = json.loads(script_tag.get_text())

# raw_product_data = json_blob["props"]["pageProps"]["initialData"]['searchResult']['itemStacks'][0]['items'][0]

# raw_product_data
#LOCATE ITEM

def locate_item(item):
    soup = make_call(item)
    script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
    json_blob = json.loads(script_tag.get_text())

    itemNum = 0
    raw_product_data = json_blob["props"]["pageProps"]["initialData"]['searchResult']['itemStacks'][0]['items'][itemNum]

    name = raw_product_data['name']
    price = raw_product_data['price']

    location = 'null'
    while location == 'null':

        try:
            raw_product_data = json_blob["props"]["pageProps"]["initialData"]['searchResult']['itemStacks'][0]['items'][itemNum]
            location = raw_product_data['productLocation'][0]['displayValue']
        except:
            location = "null"
            itemNum += 1
    

    current = product(name,price,location)
    return(current)
#PRINTS DATAFRAME

def shoppingList(shopping_list):
    list_of_locations = []

    # with open('shoppinglist.txt','rb')as f:
    #     lines = f.readlines()
    modified_list = str(shopping_list).split(",")
    
    for item in modified_list:
        list_of_locations.append(locate_item(item))
        
    df = pd.DataFrame(columns=['Item','Price','Location'])

    for object in list_of_locations:
        df2 = pd.DataFrame([{'Item': object.name, 'Price': object.price, 'Location': object.location}])
        df = pd.concat([df,df2], ignore_index=True)
        #df = df.append(df2, ignore_index=True)

    df = df.sort_values('Location')

    rtn_string = ""
    for item in list_of_locations:
        rtn_string += f'{item.name}\nPrice: ${str(item.price)}\nAisle: {item.location}\n\n'
    print(rtn_string)
    return(rtn_string)

demo = gradio.Interface(fn= shoppingList, inputs="text", outputs='text',title="Walmart Shopping helper\n(insert list separated by commas)")

demo.launch(share=True)