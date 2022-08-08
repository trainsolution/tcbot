#from ctypes.wintypes import PWIN32_FIND_DATAA
from os import remove
#from ssl import get_protocol_name
import string
from tokenize import Floatnumber
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from tabulate import tabulate
import time
import re
import pytz
valor = 100
#import tweepy

homelink=[]
bancos=[]

from datetime import date, datetime
now = datetime.now()
dia=now.date()
hora=now.time()
dia1=dia.strftime('%d/%m/%Y')
homeurl = "https://cuantoestaeldolar.pe/"
homeurl2 = "https://www.bloomberg.com/quote/USDPEN:CUR"
option2=[]
option3=[]

while((hora.hour) in range (0,23)):

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
 #print(new)

 listadatos = pd.DataFrame({
                             'PREVIO':option2[0],
                             'RANGO 52 SEMANAS':new[19][0:4]+"-"+new[20][0:4],
                             'CAMBIO 5 DIAS': new[17]+"%",
                             'ESTOCASTICO %K': new[13]
                             },index=[0])  

 print("DATOS DIARIOS REFERENCIALES")
 print(tabulate(listadatos, headers='keys', tablefmt='psql',showindex="never"))
 print("\nNota: A modo de referencia diaria, el estocástico %K mayor a 80 indicaría vender y menor a 20 indicaría comprar\n")

 for i in range(481):

       page = requests.get(homeurl,headers={"User-Agent":"Mozilla/6.0"})
       time.sleep(1)
       html_soup = BeautifulSoup(page.content,'html.parser')
       
       #time.sleep(2) #- Bloomberg
       page2 = requests.get(homeurl2,headers={'User-Agent': 'Mozilla/7.0' ,  'From': 'ok341@hotmail.com','folder': '/Browsers - Windows/Legacy Browsers','description': 'Chrome 17.0 (Win 7 64)',"browserName": "Chrome"})
       html_soup2 = BeautifulSoup(page2.content,'html.parser')

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
       
       #activar en bloomberg
       elemento2 = html_soup2.find('span', class_= "pricexText__06f600fa3e")
       time.sleep(2)
       blc=(elemento2.text)
       print("\nNuevo Precio bloomberg "+blc)

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
       #Lista 4 está ordenado en compra

       lista1.COMPRA = lista3.COMPRA.astype(str)

       #Valores máximo de compra y mínimo de venta en este momento
       vminventa = float(ordenado["VENTA"][0])
       vmaxcompra = float(lista4["COMPRA"][0])
       #print(str(vmaxcompra))

       #tabla dataframe en orden
       antesordenadov=ordenado[0:5]
       antesordenadov=antesordenadov.drop(['COMPRA'],axis=1)
       #print(antesordenadov)
       antesordenadoc=lista4[0:5]
       antesordenadoc=antesordenadoc.drop(['VENTA'],axis=1)
       #print(antesordenadoc)

       ordenado=tabulate(ordenado, headers='keys', tablefmt='psql',showindex="never")
       listab=tabulate(listab, headers='keys', tablefmt='psql',showindex="never")
       def telegram_bot_sendtext(bot_message):
              bot_token = '5381551675:AAFDvUALkEFHpY0GGB4Cr33BgukyHavwU4Y'
              bot_chatID = '-1001791296695'
              send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
              response = requests.get(send_text)
              return response.json()
       
       if valor == 100:
            
            mensaje = "HOY: "+dia1+" - EL DOLAR SE COTIZA A:\n\nONLINE COMPRA: "+ str(vmaxcompra)+"\nONLINE VENTA: "+str(vminventa)#+"\n\nPARALELO COMPRA: "+ paraleloc +"\nPARELELO VENTA: "+ paralelov  + "\n  "
            #mensaje2 = "\n              TC BANCOS              \n"
            #test = telegram_bot_sendtext(f'`{mensaje}`' + "\n" +"\nHora: " + f'```{hora2}```')
            valor=vminventa
            #print(tabulate(antesordenadov, headers='keys', tablefmt='psql',showindex="never"))
            #print(tabulate(antesordenadoc, headers='keys', tablefmt='psql',showindex="never"))
            print(mensaje)  

          
            print("Atención Desde de ahora se emitirán mensajes instantáneos para fluctuaciones mayores a S/ 0.001")
       else:
            if vminventa <= valor-0.001:
                    per=str(round((1-valor/(vminventa))*100,2))
                    #print(str(percent)+"%")
                    valorminstr=str(vminventa)
                    valorminstr2=str(vmaxcompra)
                    incr = str(round(valor - vminventa,4))

                    mensaje = "ACTUALIZACION:\nEL TIPO DE CAMBIO HA BAJADO S/ "+ incr +" / "+per+"%"+ "\nONLINE VENTA: " + valorminstr + "\nONLINE COMPRA: " + valorminstr2 #+  "\n\nPARALELO COMPRA "+ paraleloc+"\nPARALELO VENTA: "+  paralelov
                    #test = telegram_bot_sendtext(f'`{mensaje}`' + "\n" + f'```{ordenado}```'+f'`{mensaje2}`'+f'```{listab}```'+ "\nHora: "+ f'``{hora2}``')
                    #print(antesordenado[0:3])
                    valor=vminventa
                    print(mensaje)
                    dife=float(valorminstr) - float(valorminstr2)
                    print("\nEl spread actual es "+(str(round(dife,4))))
                    
            else:
                if vminventa >= valor+0.001:
                    per=str(round((1-valor/(vminventa))*100,2))
                    valorminstr=str(vminventa)
                    valorminstr2=str(vmaxcompra)
                    incr = str(round(vminventa -valor,4))
                    
                    mensaje = "ACTUALIZACION:\nEL TIPO DE CAMBIO HA SUBIDO S/ "+ incr +" / "+per+"%"+"\nONLINE VENTA: " + valorminstr + "\nONLINE COMPRA: " + valorminstr2 #+"\n\nPARALELO COMPRA "+ paraleloc+"\nPARALELO VENTA: "+ paralelov
                    #test = telegram_bot_sendtext(f'`{mensaje}`' + "\n" + f'```{ordenado}```'+"\nHora: "+f'``{hora2}``')
                    valor=vminventa
                    print(mensaje)
                    dife=float(valorminstr) - float(valorminstr2)
                    print("\nEl spread actual es "+(str(round(dife,4))))


                           
       #api.update_status("El tipo de cambio Perú se cotiza a:\n\nDolár online S/:\nCompra: "+str(vmaxcompra)+"\nVenta: "+str(vminventa)+"\n\nDólar paralelo S/:\nCompra: "+paraleloc+"\nVenta: "+paralelov+"\n\nSiguenos en Nuestro Canal de Telegram t.me/elcanaldeldolarperu para mayor información")

       #600 es 10 minutos
       #60 es 1 minuto
       
       
       print(hora2)
       print("Spread online "+str(round(vminventa-vmaxcompra,4)))
       print("Spread Bloomberg - Venta Mercado "+str(round(float(blc)-vminventa,4)))
       print("Spread Bloomberg - Compra Mercado "+str(round(float(blc)-vminventa,4)))


       t=60

       del sunatw
       del sunat
       del paraleloc
       del paralelov
       del alternop
       time.sleep(t)
