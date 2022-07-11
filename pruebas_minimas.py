
from os import remove
from ssl import get_protocol_name
import string
from tokenize import Floatnumber
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import pytz
import re
from datetime import date, datetime


now = datetime.now()
dia=now.date()
hora=now.time()

option2=[]
option3=[]

if((hora.hour) in range (8,22)):

    #Bloomberg Linea : Cierre previo

    homeurl1n="https://www.bloomberglinea.com/quote/USDPEN:CUR/"
    page1n = requests.get(homeurl1n,headers={'User-Agent': 'Mozilla/6.0' ,  'From': 'user2022@gmail.com','folder': '/Browsers - Windows/Legacy Browsers','description': 'Chrome 16.0 (Win 7 64)',"browserName": "Chrome"})
    html_soup1n = BeautifulSoup(page1n.content,'html.parser')

    elemento = html_soup1n.find_all('div', class_= "quote-details-item flex__col--sm-6 flex__col--md-4 flex__col--lg-4") 
    for var in elemento:
        new = var.find('span', class_="data-value font_sm font_medium")
        if new:
                        option2.append(new.text) 
        else:    option2.append('')
    #print(option2[0]) Cierre ayer 


    #Barchart 1: Resistencias, Soportes y otros datos
    homeurl2n = "https://www.barchart.com/forex/quotes/%5EUSDPEN/cheat-sheet"
    page2n = requests.get(homeurl2n,headers={'User-Agent': 'Mozilla/6.0' ,  'From': 'user2022@gmail.com','folder': '/Browsers - Windows/Legacy Browsers','description': 'Chrome 16.0 (Win 7 64)',"browserName": "Chrome"})
    html_soup2n = BeautifulSoup(page2n.content,'html.parser')

    elemento = html_soup2n.find('div', class_="bc-cheat-sheet") 
    new = elemento.find('cheat-sheet') #Hoja de datos largos del USDPEN
    mivar = re.findall("(\d*\.\d+|\d+.\d*)",str(new))

    #print(mivar[111]) # Máximo de 52 semanas
    #print(mivar[116]) # Retroceso del 38,2 % desde el máximo de 52 semanas, puede ser un objetivo
    #print(mivar[250]) # Mínimo de 52 semanas 
    #print(mivar[254]) # RSI 14 dias en 30%
    
    #Barchart 2: Recomendación pagina principal
    homeurl3n = "https://www.barchart.com/forex/quotes/%5EUSDPEN"
    page3n = requests.get(homeurl3n,headers={'User-Agent': 'Mozilla/6.0' ,  'From': 'user2022@gmail.com','folder': '/Browsers - Windows/Legacy Browsers','description': 'Chrome 16.0 (Win 7 64)',"browserName": "Chrome"})
    html_soup3n = BeautifulSoup(page3n.content,'html.parser')

    #elemento = html_soup3n.find('div', class_= "technical-opinion-widget clearfix") 
    #option11 = elemento.find('a', class_="buy-color")  # Recomendacion de comprar o vender

    elemento = html_soup3n.find('div', class_="bc-quote-overview row")# Cuadrito de datos pequeños
    new = re.findall("(\d*\.\d+|\d+.\d*)",str(elemento))

    listadatos = pd.DataFrame({
                                'PREVIO':option2[0],
                                'RANGO 52 SEM':option2[5],
                                'CAMBIO 5 DIAS': new[13]+"%",
                                'STOCASTICO %K': new[9]
                                },index=[0])

    print(listadatos)
