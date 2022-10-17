from audioop import reverse
from os import remove
import string
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from tabulate import tabulate
import time
import pytz
import tweepy
import urllib
import re

from datetime import date, datetime
now = datetime.now()
dia=now.date()
hora=now.time()
dia1=dia.strftime('%d/%m/%Y')
IST = pytz.timezone('America/Lima') 
t=3600

#####FUNCION BUSQUEDA DE DATOS

def scrap(homeurl):

                 option2=[]
                 option3=[]
                 resultado=[]
                 resultado2=[]
                 

                 page = requests.get(homeurl,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"})
                 html_soup1n = BeautifulSoup(page.content,'html.parser')

                #matriz compra (3 primeros paralelo)
                 elemento = html_soup1n.find_all('div', class_= "block mx-2 w-[46px] md:w-[60px] block mx-2 w-[60px]") 
                 for var in elemento:
                        new = var.find('p', class_="ValueQuotation_text___mR_0")
                        if new:
                                        option2.append(new.text)

                        else:    option2.append('')

                #matriz venta (3 primeros paralelo)
                 elemento = html_soup1n.find_all('div', class_= "block mx-2 w-[46px] md:w-[60px] mx-2 w-[60px]") 
                 for var in elemento:
                        new = var.find('p', class_="ValueQuotation_text___mR_0")
                        if new:
                                        option3.append(new.text)

                        else:    option3.append('')

        
                ##################ORDENAMIENTO
        
                 listac=sorted(option2[0:24])
                 for i in listac:
                        if(i) > '1':
                                resultado.append(i)

                 listav=sorted(option3[0:24])
                 for i in listav:
                        if(i) > '1':
                                resultado2.append(i)

                 valorminstr=float(resultado2[0])
                 valorminstr2=float(resultado.pop())
                 return valorminstr,valorminstr2

                 del option2
                 del option3
                 del listav
                 del listac

###### BARCHART 
def bar(h): 
        
        page3n = requests.get(h,headers={'User-Agent': 'Mozilla/6.0' ,  'From': 'user2022@gmail.com','folder': '/Browsers - Windows/Legacy Browsers','description': 'Chrome 16.0 (Win 7 64)',"browserName": "Chrome"})
        html_soup3n = BeautifulSoup(page3n.content,'html.parser')  
        elemento = html_soup3n.find('div', class_="bc-quote-overview row")# Cuadrito de datos pequeños
        new = re.findall("(\d*\.\d+|\d+.\d*)",str(elemento))  
        listadatos = pd.DataFrame({
                                'PRECIO CIERRE ANTERIOR':round(float(new[9]),3),
                                'RANGO ULTIMO AÑO':new[19][0:4]+" - "+new[20][0:4],
                                },index=[0])  
        listadatos.set_index('PRECIO CIERRE ANTERIOR',inplace=True)       
        lista=listadatos.T
        #lista=lista.transpose()
        #lista=tabulate(lista, headers='keys', tablefmt='psql',showindex="never")

        return lista
##################### FUNCION DEL TWEET

def twt(c,v):
        auth = tweepy.OAuth1UserHandler("Nx0020RxPlgTj6BSiRuPtXy5z", "sDJLjKxYXsVpC1nidfOeaJAdOB52F2ou6LG4wb3IupqePrdoRj","1527368196595953674-pDBuVvwRd1PZ4CssI8Fs9pqviFB8Tp", "0rMlsyMawwDtP8GsnM45zrXlyXrbquuduPXF0yUDkZdfi")
        api = tweepy.API(auth)
        try:
                api.verify_credentials()
                print("Authentication OK")
        except:
                print("Error during authentication")

        # Create API object
        api = tweepy.API(auth, wait_on_rate_limit=True)
        mensaje="El tipo de cambio Perú se cotiza a:\n\nDolár online S/:\nCompra: "+str(c)+"\nVenta: "+str(v)+"\n\nEncuéntranos en Telegram y aprovecha los cupones exclusivos t.me/elcanaldeldolarperu "
        return api.update_status(mensaje)


########################################LOGICA DE TELEGRAM

def telegram_bot_sendtext(bot_message):
                        bot_token = '5381551675:AAFDvUALkEFHpY0GGB4Cr33BgukyHavwU4Y'
                        bot_chatID = '-1001791296695'
                        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                        response = requests.get(send_text)
                        return response.json()
         
########################################LOGICA DE ENVIO


       
homeurl = "https://cuantoestaeldolar.pe/"
homeurl2= "https://www.barchart.com/forex/quotes/%5EUSDPEN"

b=[]
b=scrap(homeurl)
print(b)
c=bar(homeurl2)

while((hora.hour) in range (12,20)): #hora horario UTC
        mensajesocio2= urllib.parse.quote_plus("Aprovecha la oferta! Cambia tus dólares en inkamoney.com con el cupón CANALDOLAR y obtén un mejor tipo de cambio\nVálido hasta el 31/09/2022")
        mensajeALT="Actualizaciones del TC a partir de fluctuaciones mayores a S/ 0.01"
        mensaje ="HOY "+dia1+"\nEL DOLAR ONLINE SE COTIZA A:\n\nCOMPRA: " + str(b[1])+"\nVENTA: " + str(b[0]) + "\n\n"+str(c)+"\n\n"
        test = telegram_bot_sendtext(mensaje+mensajeALT)
        #urllib.request.urlopen(f"https://api.telegram.org/bot5381551675:AAFDvUALkEFHpY0GGB4Cr33BgukyHavwU4Y/sendMessage?chat_id=-1001791296695&text={mensajesocio2}")
        valor=b[0]
        twt(b[1],b[0])
        #print(mensaje)
                        
        time.sleep(t)
                        
        for i in range(8):
                        b=scrap(homeurl)
                        hora=now.time()
                        time.sleep(1)

                        hora2=datetime.now(IST)
                        hora2=hora2.strftime('%H:%M:%S')

                        #0.011 para evitar avisos por cambios muy pequeños de precio  
                        if b[0] <= valor-0.011:
                                
                                incr = str(round(valor - b[0],4))

                                mensaje = "ACTUALIZACION!: "+ hora2 +"\nEL DOLAR ONLINE HA BAJADO S/ "+ incr + "\nCOMPRA: " + str(b[1])+"\nVENTA: " + str(b[0]) + "\n"
                                #print(mensaje)
                                test = telegram_bot_sendtext(mensaje)
                                #urllib.request.urlopen(f"https://api.telegram.org/bot5381551675:AAFDvUALkEFHpY0GGB4Cr33BgukyHavwU4Y/sendMessage?chat_id=-1001791296695&text={mensajesocio2}")
                                valor=b[0]
                                twt(b[1],b[0])
                                
                        else:
                                if b[0] >= valor+0.011:
                                        
                                        incr = str(round(b[0] -valor,4))
                                        mensaje = "ACTUALIZACION!: "+ hora2 +"\nEL DOLAR ONLINE HA SUBIDO S/ "+ incr + "\nCOMPRA: " + str(b[1])+ "\nVENTA: " + str(b[0]) + "\n"
                                        test = telegram_bot_sendtext(mensaje)
                                        #urllib.request.urlopen(f"https://api.telegram.org/bot5381551675:AAFDvUALkEFHpY0GGB4Cr33BgukyHavwU4Y/sendMessage?chat_id=-1001791296695&text={mensajesocio2}")
                                        print(mensaje)
                                        valor=b[0]
                                        twt(b[1],b[0])
                        print("Este el contador: "+str(i))
                        time.sleep(t)
                        
        print("Se acabó el script por hoy")
        time.sleep(86400)                  
        


                