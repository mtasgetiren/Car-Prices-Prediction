# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 11:45:48 2020

@author: m_tasgetiren
"""



import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook
from datetime import datetime,date, timedelta
import time
import pandas as pd
from pandas.io import gbq



from selenium import webdriver
from selenium.webdriver.chrome.options import Options

basla=datetime.now()
#Driver path of chrome driver
driver_path = ""
capabilities = { 'chromeOptions':  { 'useAutomationExtension': False}}
browser = webdriver.Chrome(executable_path=driver_path,desired_capabilities = capabilities)
chrome_options = Options()
chrome_options.headless=True
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
datetime_now = datetime.now().replace(hour=00, minute=00,second=0,microsecond=0)

 
araba_listesi=[ 'audi-a3-a3-sedan', 'audi-a3-a3-sportback',
               'bmw-1-serisi','bmw-3-serisi','bmw-5-serisi',
               'chevrolet-cruze',
               'citroen-c3','citroen-c4','citroen-c-elysee',
               'dacia-logan','dacia-sandero',
               'fiat-albea','fiat-egea','fiat-linea','fiat-palio','fiat-punto',
               'ford-fiesta','ford-focus','ford-mondeo',
               'honda-civic',
               'hyundai-accent','hyundai-accent-blue','hyundai-accent-era','hyundai-elantra','hyundai-i20','hyundai-i30',
               'kia-ceed','kia-rio',
               'mercedes-benz-a-serisi','mercedes-benz-c-serisi','mercedes-benz-e-serisi','mercedes-benz-s-serisi',
               'mini-cooper','nissan-micra',
               'opel-astra','opel-corsa','opel-insignia','opel-vectra',
               'peugeot-206','peugeot-207','peugeot-301','peugeot-307','peugeot-308',
               'renault-clio', 'renault-fluence','renault-megane','renault-symbol',
               'seat-ibiza','seat-leon',
               'skoda-fabia','skoda-octavia','skoda-superb',
               'toyota-auris','toyota-corolla','toyota-yaris','toyota-avensis',
               'volkswagen-golf','volkswagen-jetta','volkswagen-passat','volkswagen-polo','volkswagen-vw-cc',
               'volvo-s60','volvo-s40'
               ]
url_list=[]

for i in araba_listesi:
    url1="https://www.sahibinden.com/"+ i+ "/dizel/manuel?pagingSize=50"
    url2="https://www.sahibinden.com/"+ i+ "/benzin/manuel?pagingSize=50"
    url3="https://www.sahibinden.com/"+ i+ "/dizel/yari-otomatik,otomatik?pagingSize=50"
    url4="https://www.sahibinden.com/"+ i+ "/benzin/yari-otomatik,otomatik?pagingSize=50"
    url_list.append(url1)
    url_list.append(url2)
    url_list.append(url3)
    url_list.append(url4)

yakit_cesit=["dizel","benzin"]
vites_cesit=["manuel","otomatik"]

uzunluk=len(url_list[0])
for url in url_list:
   # url="https://www.sahibinden.com.tr/sut-c-6c"
    browser.get(url)
    time.sleep(2)
    bit=datetime.now()
    print(bit-basla) 
       
    print(url)
#    sahibinden_r=requests.get(url)
#    sahibinden_soup= BeautifulSoup(sahibinden_r.text , 'html.parser')
    sahibinden_soup= BeautifulSoup(browser.page_source , 'lxml')
    product_page_num=sahibinden_soup.findAll('p',{'class':'mbdef'})
    if len(product_page_num)==0:
        continue
    max_page=int(product_page_num[0].text.strip().split()[1])
   
    if max_page>20 :
       max_page=20
       
    inserted_values=[]  
    
    for i in range(1, max_page+1):
        
        url=url+"&pagingOffset="+ str((i-1)*50)
#        print(url)
        browser.get(url)
        time.sleep(3)
 
        sahibinden_soup= BeautifulSoup(browser.page_source , 'lxml')
        product_id=sahibinden_soup.findAll('tbody',{'class':'searchResultsRowClass'})
        product_model=sahibinden_soup.findAll('td',{'class':'searchResultsTagAttributeValue'})
        product_name=sahibinden_soup.findAll('a',{'class':'classifiedTitle'})
        product_attrs=sahibinden_soup.findAll('td',{'class':'searchResultsAttributeValue'})
        product_prices=sahibinden_soup.findAll('td',{'class':'searchResultsPriceValue'})
        product_date=sahibinden_soup.findAll('td',{'class':'searchResultsDateValue'})
        product_loc=sahibinden_soup.findAll('td',{'class':'searchResultsLocationValue'})

    
        v=0
        k=0
        for i in range(len(product_name)):
      
             model=product_model[i].text.strip()
             name=product_name[i].text.strip()
             yıl=product_attrs[v].text.strip()
             v=v+1
             km_1=product_attrs[v].text.strip()
             if km_1 == "":
                 km=""
             else:
                 km=int(product_attrs[v].text.strip().replace('.',''))
             v=v+1
             renk=product_attrs[v].text.strip()
             v=v+1
    
             price=int(product_prices[i].text.strip()[:-2].replace('.','').split(',')[0])
    
             tarih=product_date[i].text.strip()
             if product_loc[i].text.strip()=="Diğer":
                 loc="Diger"
             else:    
                 loc=str(product_loc[i]).split(">")[1].split("<")[0].split("\n")[1].split()[0]
             id=product_id[0].findAll(attrs={"data-id": True})[i]['data-id'] 
             
             marka=url.split("com/")[1].split("/")[0]
             yakit=[i for i in yakit_cesit if i in url][0]       
             vites=[i for i in vites_cesit if i in url][0]
             
             insert_val={'COLL_DATE': datetime_now, 
                         'MODEL': model,
                         'YIL': yıl, 'KM': km, 'RENK': renk, 'FIYAT': price, 
                         'ILAN_TARIHI':tarih,
                         'IL_ILCE': loc, 
                         'ID': id,
                         'YAKIT':yakit,
                         'VITES':vites,
                         'MARKA':marka}
             if km !="" and model !="" and yıl !="" and renk !=""  and price !="" and tarih  !="" and marka !="" and  loc !="":                                 
                 inserted_values.append(insert_val)
             df = pd.DataFrame(inserted_values)
             convert_dict = {'YIL':'int64','ID':'int64','KM':float,'FIYAT':'int64'
                             } 
             df = df.astype(convert_dict)
             
 
        url=url.split("&pagingOffset")[0]
   

    #type the path here.    
    df.to_excel("")  
    
    df = df[0:0] 
browser.close()        
