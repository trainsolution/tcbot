#from cgi import test
#from re import A
from ctypes.wintypes import PWIN32_FIND_DATAA
from os import remove
from ssl import get_protocol_name
import string
from tokenize import Floatnumber
#from typing import get_args
#from attr import attrs
from bs4 import BeautifulSoup
import requests
import pandas as pd
#import csv
import numpy as np
from tabulate import tabulate
import time
#import gc 
import pytz
valor = 100
import tweepy

homelink=[]
bancos=[]

from datetime import date, datetime
now = datetime.now()
dia=now.date()
hora=now.time()
dia1=dia.strftime('%d/%m/%Y')
#hora1=hora.strftime('%H:%M:%S')
homeurl = "https://cuantoestaeldolar.pe/"
homeurl2 = "https://www.bloomberg.com/quote/USDPEN:CUR"

while((hora.hour) in range (13,20)): #hora horario UTC

 for i in range(601):
       page = requests.get(homeurl,headers={"User-Agent":"Mozilla/6.0"})
       time.sleep(2)
       html_soup = BeautifulSoup(page.content,'html.parser')
      # time.sleep(2)
       #page2 = requests.get(homeurl2,headers={'User-Agent': 'Mozilla/6.0' ,  'From': 'user2022@gmail.com','folder': '/Browsers - Windows/Legacy Browsers','description': 'Chrome 16.0 (Win 7 64)',"browserName": "Chrome"})
       #html_soup2 = BeautifulSoup(page2.content,'html.parser')


       precioc=[]
       preciov=[]
       ncasa=[]
       alternop=[]
       alternop2=[]
       sunatw=[]
       palternov=[]
       banco1c=[]
       banco2c=[]
       bancotc=[]
       bancotv=[]
       banco1v=[]
       banco2v=[]
       banksname=['BCP','INTERBANK','BBVA','SCOTIA','B. DE LA NACION']
       now = datetime.now()
       hora=now.time()
       #hora1=hora.strftime('%H:%M:%S') 
       IST = pytz.timezone('America/Lima') 
       hora2=datetime.now(IST)
       hora2=hora2.strftime('%H:%M:%S')
       
       
       elemento = html_soup.find_all('div', class_= "wrapper-table tb_dollar t-odd tb_hidden-") 

       for var1 in elemento:
              
              #sección dolar paralelo

              arribaizq2 = var1.find('div', class_="td tb_dollar_compra tb_dollar__",src="")
              if arribaizq2:
                     alternop2.append(arribaizq2.text) #tabla
                     arribaizq2=arribaizq2.text 
              else: alternop2.append('')

              arribaizq = var1.find('div', class_="td tb_dollar_venta tb_dollar__",src="")
              if arribaizq:
                     alternop.append(arribaizq.text) #tabla
                     arribaizq=arribaizq.text 
              else: alternop.append('')

       elemento = html_soup.find_all('div', class_="wrapper-table tb_dollar tb_hidden-")
       
       for var1 in elemento:
              #para precio dolar sunat
              arribam = var1.find('div', class_="td tb_dollar_venta tb_dollar__",src="")
              if arribam:
                      sunatw.append(arribam.text) #tabla
                      arribam=arribam.text        
              else: sunatw.append('')
  
       #seccion casas de cambio
       elemento = html_soup.find_all('div', class_= "wrapper-table tb_dollar") 

       for var1 in elemento:

              nombrecasa = var1.find('h3', target="")
              if nombrecasa:
                     ncasa.append(nombrecasa.text) #tabla
                     nombrecasa=nombrecasa.text        
              else: ncasa.append('')
       
              pcompra = var1.find('div', class_="td tb_dollar_compra")
              if pcompra:
                     precioc.append(pcompra.text) #tabla
                     pcompra=pcompra.text         
              else: precioc.append('') 
       
              pventa = var1.find('div', class_="td tb_dollar_venta")
       
              if pventa:
                     preciov.append(pventa.text) #tabla
                     pventa=pventa.text
              else:    preciov.append('')


       #seción bancos even
       elemento = html_soup.find_all('div', class_= "wrapper-table tb_dollar t-even tb_hidden-") 
       
       for var1 in elemento:
              bank1c = var1.find('div', class_="td tb_dollar_compra")
              
              if bank1c:
                     banco1c.append(bank1c.text) 
                     #print(banco1c)
                     bank1c=bank1c.text
              else:    banco1c.append('')

              bank1v = var1.find('div', class_="td tb_dollar_venta")
              
              if bank1v:
                     banco1v.append(bank1v.text) 
                     bank1v=bank1v.text
              else:    banco1v.append('')



       #seción bancos odd
       elemento = html_soup.find_all('div', class_= "wrapper-table tb_dollar t-odd tb_hidden-") 
       
       for var1 in elemento:
              bank2c = var1.find('div', class_="td tb_dollar_compra")
              
              if bank2c:
                     banco2c.append(bank2c.text) 
                     bank2c=bank2c.text
              else:    banco2c.append('')
             
              bank2v = var1.find('div', class_="td tb_dollar_venta")
             
              if bank2v:
                     banco2v.append(bank2v.text) 
                     bank2v=bank2v.text
              else:    banco2v.append('')


     
       bancotc = banco1c + banco2c
       bancotc[::2]=banco1c
       bancotc[1::2]=banco2c

       bancotv = banco1v + banco2v
       bancotv[::2]=banco1v
       bancotv[1::2]=banco2v

       bancotv2=[]
       for esp in bancotv:
              result = esp.replace('S/.','S/')
              bancotv2.append(result)
      
     
       
       # define elementos a reemplazar: vacio, salto de pagina y BCP
       removet=str.maketrans('',"",'\n')
       removet2=str.maketrans('',"","BCP")
       removet3=str.maketrans('$',' ','S/')
       # reemplaza

       ncasa=[s.translate(removet) for s in ncasa]
       precioc=[s.translate(removet) for s in precioc]
       preciov=[s.translate(removet) for s in preciov]
       homelink=[s.translate(removet) for s in homelink]
       bancos=[s.translate(removet) for s in bancos]
       alternop=[s.translate(removet) for s in alternop]
       alternop2=[s.translate(removet) for s in alternop2]
       sunatw=[s.translate(removet) for s in sunatw]
       banco1c=[s.translate(removet) for s in banco1c]
       banco2c=[s.translate(removet) for s in banco2c]
       banco1v=[s.translate(removet) for s in banco1v]
       banco2v=[s.translate(removet) for s in banco2v]
       bancotc=[s.translate(removet) for s in bancotc]
       bancotc=[s.translate(removet3) for s in bancotc]
       bancotv2=[s.translate(removet) for s in bancotv2]
       bancotv2=[s.translate(removet3) for s in bancotv2]
       
       bancotc=[item for item in bancotc if len(item)>0]
       bancotv2=[item for item in bancotv2 if len(item)>0]

       

       paralelov=alternop[0]
       paralelov=paralelov[3:8]
       paraleloc=alternop2[0]
       paraleloc=paraleloc[1:6]
       sunat=sunatw[0]
       sunat=sunat[3:8]
     

       lista1 = pd.DataFrame({
                            'NOMBRE':ncasa,
                            'COMPRA':precioc,
                            'VENTA': preciov,
                     #       'URL': homelink,
                     #       'BANCOS':bancos,
                     #      'FECHA': dia1,
                     #       'HORA': hora1
                            })

       
       
       listab = pd.DataFrame({
                            'NOMBRE': banksname,
                            'COMPRA': bancotc,
                            'VENTA': bancotv2,


       })

       del ncasa
       del precioc
       del preciov
       del banco1c
       del banco2c
       del banco1v
       del banco2v
       del bancotc
       del bancotv
       del bancotv2
       
      # elemento2 = html_soup2.find('span', class_= "priceText__06f600fa3e")
       #time.sleep(2)
       
     #  blc=(elemento2.text)

       #filtros y ordenamiento
       filtro = lista1['NOMBRE'] != ""
       lista1 = lista1[filtro]
       filtro2 = lista1['VENTA'] != "0.000"
       lista1 = lista1[filtro2]
       
       filtro3 = lista1['VENTA'] != "0.0000"
       lista1 = lista1[filtro3]
       filtro4 = lista1['NOMBRE'] != "Rapidex"
       lista1 = lista1[filtro4]
       #filtro5 = lista1['NOMBRE'] != "Kaspay"
       #lista1 = lista1[filtro5]
       filtro6 = lista1['NOMBRE'] != "Letsbit"
       lista1 = lista1[filtro6]


       lista1.VENTA = lista1.VENTA.astype(float)
       lista2=lista1.sort_values(by=['VENTA'], kind="mergesort",ascending=True)
       lista1.VENTA = lista1.VENTA.astype(str)
      
       ordenado=lista2.reset_index(level=None, drop=True, inplace=False, col_level=0, col_fill='')
       
       lista1.COMPRA = lista1.COMPRA.astype(float)
       lista3=lista1.sort_values(by=['COMPRA'], kind="mergesort",ascending=False)
       lista4=lista3.reset_index(level=None, drop=True, inplace=False, col_level=0, col_fill='')
       lista1.COMPRA = lista3.COMPRA.astype(str)

       print(hora2)

       #Valores máximo de compra y mínimo de venta en este momento
       vminventa = float(ordenado["VENTA"][0])
       vmaxcompra = float(lista4["COMPRA"][0])

       #tabla dataframe en orden
       ordenado=tabulate(ordenado, headers='keys', tablefmt='psql',showindex="never")
       listab=tabulate(listab, headers='keys', tablefmt='psql',showindex="never")
       def telegram_bot_sendtext(bot_message):
              bot_token = '5381551675:AAFDvUALkEFHpY0GGB4Cr33BgukyHavwU4Y'
              bot_chatID = '-1001791296695'
              send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
              response = requests.get(send_text)
              return response.json()
       
       if valor == 100:
            valorminstr=str(vminventa)
            valorminstr2=str(vmaxcompra)
            mensaje = "EL DOLAR SE COTIZA A:\nPARALELO COMPRA "+ paraleloc +"\nPARELELO VENTA: "+ paralelov  +  "\n\n     - TC CASAS DE CAMBIO ONLINE -    "
            mensaje2 = "\n              TC BANCOS              \n"
            test = telegram_bot_sendtext(f'`{mensaje}`' + "\n" + f'```{ordenado}```'+f'`{mensaje2}`'+f'```{listab}```'+"\nHora: " + f'```{hora2}```')
            valor=vminventa
            #print(ordenado)
       else:
            #0.003 para evitar avisos por cambios muy pequeños de precio  
            if vminventa <= valor-0.01:
                    
                    valorminstr=str(vminventa)
                    valorminstr2=str(vmaxcompra)
                    incr = str(round(valor - vminventa,4))

                    mensaje = "ACTUALIZACION\nEL P. DE VENTA ONLINE HA BAJADO S/"+ incr + "\nONLINE VENTA MINIMO ACTUAL: " + valorminstr + "\n\nPARALELO COMPRA "+ paraleloc+"\nPARALELO VENTA: "+  paralelov +"\n\n     - TC CASAS DE CAMBIO ONLINE -    "
                    test = telegram_bot_sendtext(f'`{mensaje}`' + "\n" + f'```{ordenado}```'+"\nHora: "+ f'``{hora2}``')
                    valor=vminventa
                    
            else:
                if vminventa >= valor+0.01:
                        
                    
                    valorminstr=str(vminventa)
                    valorminstr2=str(vmaxcompra)
                    incr = str(round(vminventa -valor,4))
                    
                    mensaje = "ACTUALIZACION\nEL P. DE VENTA ONLINE HA SUBIDO S/"+ incr + "\nONLINE VENTA MINIMO ACTUAL: " + valorminstr + "\n\nPARALELO COMPRA "+ paraleloc+"\nPARALELO VENTA: "+ paralelov +"\n\n     - TC CASAS DE CAMBIO ONLINE -    "
                    test = telegram_bot_sendtext(f'`{mensaje}`' + "\n" + f'```{ordenado}```'+"\nHora: "+f'``{hora2}``')
                    valor=vminventa
       
       
       #600 es 10 minutos
       #60 es 1 minuto
       #print(hora.hour)
       #if hora.hour > 12:
              #t=3600
              
       #else:
       t=3600

       auth = tweepy.OAuth1UserHandler("Nx0020RxPlgTj6BSiRuPtXy5z", "sDJLjKxYXsVpC1nidfOeaJAdOB52F2ou6LG4wb3IupqePrdoRj","1527368196595953674-pDBuVvwRd1PZ4CssI8Fs9pqviFB8Tp", "0rMlsyMawwDtP8GsnM45zrXlyXrbquuduPXF0yUDkZdfi")
       
       api = tweepy.API(auth)
       try:
              api.verify_credentials()
              print("Authentication OK")
       except:
              print("Error during authentication")

       # Create API object
       api = tweepy.API(auth, wait_on_rate_limit=True)

       api.update_status("El tipo de cambio Perú se cotiza a:\n\nDolár online S/:\nCompra: "+str(vmaxcompra)+"\nVenta: "+str(vminventa)+"\n\nDólar paralelo S/:\nCompra: "+paraleloc+"\nVenta: "+paralelov+"\n\nSiguenos en Nuestro Canal de Telegram t.me/elcanaldeldolarperu para mayor información")

       del sunatw
       del sunat
       del paraleloc
       del paralelov
       del alternop
       time.sleep(t)