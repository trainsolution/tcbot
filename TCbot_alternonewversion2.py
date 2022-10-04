
from audioop import reverse
from os import remove
from ssl import get_protocol_name
import string
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from tabulate import tabulate
import time
import pytz
valor = 100
import tweepy
import urllib
import re

from datetime import date, datetime
now = datetime.now()
dia=now.date()
hora=now.time()
dia1=dia.strftime('%d/%m/%Y')
IST = pytz.timezone('America/Lima') 

valor=100

#####BUSQUEDA DE DATOS

homeurl = "https://cuantoestaeldolar.pe/"
homeurl2= "https://www.barchart.com/forex/quotes/%5EUSDPEN"

#Barchart 2: Recomendación pagina principal
page3n = requests.get(homeurl2,headers={'User-Agent': 'Mozilla/6.0' ,  'From': 'user2022@gmail.com','folder': '/Browsers - Windows/Legacy Browsers','description': 'Chrome 16.0 (Win 7 64)',"browserName": "Chrome"})
html_soup3n = BeautifulSoup(page3n.content,'html.parser')  
elemento = html_soup3n.find('div', class_="bc-quote-overview row")# Cuadrito de datos pequeños
new = re.findall("(\d*\.\d+|\d+.\d*)",str(elemento))  


listadatos = pd.DataFrame({
                             'CIERRE DE AYER':round(float(new[9]),3),
                             'RANGO ULTIMAS 52 SEMANAS (1 AÑO)':new[19][0:4]+"-"+new[20][0:4],
                             },index=[0])  
print(listadatos)

while((hora.hour) in range (0,24)): #hora horario UTC


    for i in range(8):
        option2=[]
        option3=[]
        resultado=[]
        resultado2=[]
        hora2=datetime.now(IST)
        hora2=hora2.strftime('%H:%M:%S')


        page = requests.get(homeurl,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"})
        html_soup1n = BeautifulSoup(page.content,'html.parser')

        #matriz compra (3 primeros paralelo)
        elemento = html_soup1n.find_all('div', class_= "block mx-2 w-[46px] md:w-[60px] block mx-2 w-[60px]") 

        for var in elemento:
                new = var.find('p', class_="ValueQuotation_text___mR_0")
                if new:
                                option2.append(new.text)

                else:    option2.append('')
        print(option2)
        #matriz venta (3 primeros paralelo)
        elemento = html_soup1n.find_all('div', class_=  "block mx-2 w-[46px] md:w-[60px] mx-2 w-[60px]") 
        for var in elemento:
                new = var.find('p', class_="ValueQuotation_text___mR_0")
                if new:
                                option3.append(new.text)

                else:    option3.append('')

        #matriz nombre      
        elemento = html_soup1n.find_all('div', class_= "w-[90px] md:w-36 h-auto flex align-middle justify-center") 
        for var in elemento:   
                str_match = re.findall(r'(\w*)(.svg|.png)',str(elemento))
                df = pd.DataFrame(str_match, columns = ['Names','Data'])

        filtro = df['Names'] != "image"
        df=df[filtro]

        filtro = df['Names'] != "3"
        df=df[filtro]

        filtro = df['Names'] != "2000"
        df=df[filtro]

    
        df=df.drop_duplicates()
        df.reset_index(drop=True,inplace=True)

        
        df.Names.replace({"v2": "Dollar House", "cambiafx_v2": "CambiaFx","2": "Securex","capital": "VipCapital","instakash_v2": "Instakash","union": "Western Union"},inplace=True)      
        ind = df[df.duplicated('Names')].index[0]
        df.Names[ind]="HayCambio"
        df.Names.replace({"cambio": "SrCambio","adol":"Adolfo Exchange"},inplace=True)   


        ##################ORDENAMIENTO DE LISTAS Y DATAFRAMES
        # Dolar paralelo
        #paraleloc=option2[1]
        #paralelov=option3[1]

        # Eliminar dolar paralelo de la tabla
        #option2.pop(0)
        #option2.pop(0)
        #option2.pop(0)
        #option3.pop(0)
        #option3.pop(0)
        #option3.pop(0)

        #conversion a Dataframe de las listas         
        dfc = pd.DataFrame(option2[0:25], columns = ['Compra'])
        dfv = pd.DataFrame(option3[0:25], columns = ['Venta'])
        #union de Dataframes
        dft=pd.concat([df, dfc, dfv], axis=1)
        #print(dft)

        
        dft.Venta = dft.Venta.astype(float)
        dft2=dft.sort_values(by=['Venta'], kind="mergesort",ascending=True)
        dft.Venta = dft.Venta.astype(str)
        
        print(dft2)

        #Seleccion de valores mayores a 1 en las listas
        listac=sorted(option2[0:24])
        
        for i in listac:
                if(i) > '1':
                        resultado.append(i)
                

        listav=sorted(option3[0:24])

        for i in listav:
                if(i) > '1':
                        resultado2.append(i)

        ########################################LOGICA DE ENVIO

        def telegram_bot_sendtext(bot_message):
                    bot_token = '5381551675:AAFDvUALkEFHpY0GGB4Cr33BgukyHavwU4Y'
                    bot_chatID = '811650091'
                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                    response = requests.get(send_text)
                    return response.json()
        
        valorminstr=float(resultado2[0])
        valorminstr2=float(resultado.pop())
        mensajesocio2= urllib.parse.quote_plus("Aprovecha la oferta! Cambia tus dólares en inkamoney.com con el cupón INKADOLAR y obtén un mejor tipo de cambio\nVálido hasta el 31/09/2022")
        mensajeinicial="Se enviarán mensajes de actualizaciones por cada fluctuación de S/ 0.05 en el TC"
        ordenado=tabulate(listadatos, headers='keys', tablefmt='psql',showindex="never")


        if valor == 100:
                
                    mensaje ="HOY "+dia1+"\nEL DOLAR ONLINE SE COTIZA A:\n\nCOMPRA: " + str(valorminstr2)+"\nVENTA: " + str(valorminstr) + "\n\n"
                    test = telegram_bot_sendtext(mensaje+f'`{ordenado}`'+"\n" +mensajeinicial)
                    #urllib.request.urlopen(f"https://api.telegram.org/bot5381551675:AAFDvUALkEFHpY0GGB4Cr33BgukyHavwU4Y/sendMessage?chat_id=-1001791296695&text={mensajesocio2}")
                    valor=valorminstr
                    print(mensaje)
        else:
                    #0.005 para evitar avisos por cambios muy pequeños de precio  
                    if valorminstr <= valor-0.06:
                            
                            incr = str(round(valor - valorminstr,4))

                            mensaje = "ACTUALIZACION!"+ hora2 +"\nEL DOLAR ONLINE HA BAJADO S/ "+ incr + "\nCOMPRA: " + str(valorminstr2)+"\nVENTA: " + str(valorminstr) + "\n"
                            print(mensaje)
                            test = telegram_bot_sendtext(mensaje)
                            #urllib.request.urlopen(f"https://api.telegram.org/bot5381551675:AAFDvUALkEFHpY0GGB4Cr33BgukyHavwU4Y/sendMessage?chat_id=-1001791296695&text={mensajesocio2}")
                            valor=valorminstr
                            
                    else:
                        if valorminstr >= valor+0.06:
                                
                            incr = str(round(valorminstr -valor,4))
                            
                            mensaje = "ACTUALIZACION!"+ hora2 +"\nEL DOLAR ONLINE HA SUBIDO S/ "+ incr + "\nCOMPRA: " + str(valorminstr2)+ "\nVENTA: " + str(valorminstr) + "\n"
                            test = telegram_bot_sendtext(mensaje)
                            #urllib.request.urlopen(f"https://api.telegram.org/bot5381551675:AAFDvUALkEFHpY0GGB4Cr33BgukyHavwU4Y/sendMessage?chat_id=-1001791296695&text={mensajesocio2}")
                            print(mensaje)
                            valor=valorminstr
        del option2
        del option3
        del listav
        del listac
        
        t=10

        time.sleep(t)
        