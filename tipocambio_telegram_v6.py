from cgi import test
from re import A
from ssl import get_protocol_name
import string
from tokenize import Floatnumber
from typing import get_args
from attr import attrs
from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
import numpy as np
from tabulate import tabulate
import time
import gc 

valor = 100

homelink=[]
bancos=[]

from datetime import date, datetime
now = datetime.now()
dia=now.date()
hora=now.time()
#hora = datetime.utcfromtimestamp(hora)
dia1=dia.strftime('%d/%m/%Y')
hora1=hora.strftime('%H:%M:%S')
homeurl = "https://cuantoestaeldolar.pe/"

for i in range(601):
       page = requests.get(homeurl)
       html_soup = BeautifulSoup(page.content,'html.parser')
       precioc=[]
       preciov=[]
       ncasa=[]
       alternop=[]
       sunatw=[]
       palternov=[]
       now = datetime.now()
       hora=now.time()
       hora1=hora.strftime('%H:%M:%S') 
       
       elemento = html_soup.find_all('div', class_= "wrapper-table tb_dollar t-odd tb_hidden-") 

       for var1 in elemento:
              
              #para precio dolar paralelo
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
                      print(sunatw)
                      arribam=arribam.text        
              else: sunatw.append('')
  

       elemento = html_soup.find_all('div', class_= "wrapper-table tb_dollar") #seccion de interes por datos

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

              link = var1.find('a', rel="nofollow")
              if link:
                     homelink.append(link['href']) #tabla
                     link=link.text
              else:    homelink.append('')

              banks = var1.find('div', class_="wrapper-table") 
              if banks:
                     bancos.append(banks.text) #tabla
                     banks=banks.text
              #else:    bancos.append('')

       # define elementos a reemplazar: vacio, salto de pagina y BCP
       removet=str.maketrans('',"",'\n')
       removet2=str.maketrans('',"","BCP")

       # reemplaza

       ncasa=[s.translate(removet) for s in ncasa]
       precioc=[s.translate(removet) for s in precioc]
       preciov=[s.translate(removet) for s in preciov]
       homelink=[s.translate(removet) for s in homelink]
       bancos=[s.translate(removet) for s in bancos]
       alternop=[s.translate(removet) for s in alternop]
       sunatw=[s.translate(removet) for s in sunatw]
       paralelo=alternop[0]
       paralelo=paralelo[3:8]
       sunat=sunatw[0]
       sunat=sunat[3:8]
       print(sunat)

       lista1 = pd.DataFrame({
                            'NOMBRE':ncasa,
                            'COMPRA':precioc,
                            'VENTA': preciov,
                     #       'URL': homelink,
                     #       'BANCOS':bancos,
                     #      'FECHA': dia1,
                     #       'HORA': hora1
                            })

       del ncasa
       del precioc
       del preciov

       # escrito en csv
       lista1.to_csv(r'C:\DISCO G\SINCRONIZACION\CURSOS FINANCIEROS\webscrap\lista_tc3.csv', index=None, header=True, encoding='utf-8-sig')
       filtro = lista1['NOMBRE'] != ""
       lista1 = lista1[filtro]
       filtro2 = lista1['VENTA'] != "0.000"
       lista1 = lista1[filtro2]
       
       lista1.VENTA = lista1.VENTA.astype(float)
       lista2=lista1.sort_values(by=['VENTA'], kind="mergesort",ascending=True)
       time.sleep(2)
       lista1.VENTA = lista1.VENTA.astype(str)
       #print(lista2)
       ordenado=lista2.reset_index(level=None, drop=True, inplace=False, col_level=0, col_fill='')
       
       lista1.COMPRA = lista1.COMPRA.astype(float)
       lista3=lista1.sort_values(by=['COMPRA'], kind="mergesort",ascending=True)
       time.sleep(2)
       lista1.COMPRA = lista1.COMPRA.astype(str)

       print(hora1)
      

       #tabla dataframe en orden
       vminventa = float(ordenado["VENTA"][0])
       vmincompra = float(lista1["COMPRA"][0])
       
       ordenado=tabulate(ordenado, headers='keys', tablefmt='psql',showindex="never")

       def telegram_bot_sendtext(bot_message):
              bot_token = '5381551675:AAFDvUALkEFHpY0GGB4Cr33BgukyHavwU4Y'
              bot_chatID = '-1001791296695'
              send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
              response = requests.get(send_text)
              return response.json()
       
       if valor == 100:
            valorminstr=str(vminventa)
            valormaxstr=str(vmincompra)
            mensaje = "DOLAR VENTA SE COTIZA A:\nPARALELO "+ paralelo + "\nMINIMO ONLINE S/ " + valorminstr +"\nSUNAT "+sunat +"\nHora: " + hora1 + "\nLISTADO TC ONLINE"
            test = telegram_bot_sendtext(f'`{mensaje}`' + "\n" + f'```{ordenado}```')
            valor=vminventa
       else:
            if vminventa < valor:
                    #test = telegram_bot_sendtext("\n".join(ordenado['NOMBRE']+" "+ordenado['COMPRA']+" "+ordenado['VENTA']))
                    valorminstr=str(vminventa)
                    valormaxstr=str(vmincompra)
                    incr = str(round(valor - vminventa,4))
                    mensaje = "ALERTA - EL DOLAR HA BAJADO "+ incr + "\nPARALELO "+ paralelo +"\nMINIMO ONLINE S/ " + valorminstr + "\nCOMPRA MINIMO "+ valormaxstr +"\nSUNAT "+sunat +"\nHora: " + hora1
                    test = telegram_bot_sendtext(f'`{mensaje}`' + "\n" + f'```{ordenado}```')
                    valor=vminventa
                    incr=valor-vminventa 
            else:
                if vminventa > valor:
                        
                    #test = telegram_bot_sendtext("\n".join(ordenado['NOMBRE']+" "+ordenado['COMPRA']+" "+ordenado['VENTA']))
                    valorminstr=str(vminventa)
                    valormaxstr=str(vmincompra)
                    incr = str(round(vminventa -valor,4))
                    
                    mensaje = "ALERTA - EL DOLAR HA SUBIDO "+ incr + "\nPARALELO "+ paralelo +"\nMINIMO ONLINE S/ " + valorminstr +"\nCOMPRA MAXIMO "+ valormaxstr +"\nSUNAT "+sunat +"\nHora: " + hora1 
                    test = telegram_bot_sendtext(f'`{mensaje}`' + "\n" + f'```{ordenado}```')
                    valor=vminventa
       del sunatw
       del sunat
       del paralelo
       del alternop
       
     #  lista1=lista1.drop(range(0,19),axis=0)
       #print(lista1)
      # del lista1
      #   del ordenado
      #  gc.collect()
      #   lista1=pd.DataFrame()
      #  ordenado=pd.DataFrame()
      # print(lista1)

       time.sleep(10)