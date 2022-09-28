
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




#print("List before calling remove() function:")
#print(listo)

#listo=list(set(listo))

#print("List after calling remove() function:")
#print(listo)


while((hora.hour) in range (8,20)): #hora horario UTC


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
        print(elemento)

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
        #paraleloc=option2[1]
        #paralelov=option3[1]

        #option2.pop(0)
        #option2.pop(0)
        #option2.pop(0)
        listac=sorted(option2[0:24])
        
        for i in listac:
                if(i) > '1':
                        resultado.append(i)
        #print(resultado)
                
        #option3.pop(0)
        #option3.pop(0)
        #option3.pop(0)
        listav=sorted(option3[0:24])

        for i in listav:
                if(i) > '1':
                        resultado2.append(i)
        #print(resultado2)

        ########################################LOGICA DE ENVIO

        def telegram_bot_sendtext(bot_message):
                    bot_token = '5381551675:AAFDvUALkEFHpY0GGB4Cr33BgukyHavwU4Y'
                    bot_chatID = '-1001791296695'
                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                    response = requests.get(send_text)
                    return response.json()
        
        valorminstr=float(resultado2[0])
        valorminstr2=float(resultado.pop())
        mensajesocio2= urllib.parse.quote_plus("Aprovecha la oferta! Cambia tus dólares en inkamoney.com con el cupón CANALDOLAR y obtén un mejor tipo de cambio\nVálido hasta el 31/09/2022")



        if valor == 100:
                
                    mensaje ="HOY "+dia1+"\nEL DOLAR ONLINE SE COTIZA A:\nCOMPRA: " + str(valorminstr2)+"\nVENTA: " + str(valorminstr) + "\n\n"
                    test = telegram_bot_sendtext(mensaje)
                    #urllib.request.urlopen(f"https://api.telegram.org/bot5381551675:AAFDvUALkEFHpY0GGB4Cr33BgukyHavwU4Y/sendMessage?chat_id=-1001791296695&text={mensajesocio2}")
                    valor=valorminstr
                    print(mensaje)
        else:
                    #0.003 para evitar avisos por cambios muy pequeños de precio  
                    if valorminstr <= valor-0.011:
                            
                            incr = str(round(valor - valorminstr,4))

                            mensaje = "ACTUALIZACION!: "+ hora2 +"\nEL DOLAR ONLINE HA BAJADO S/ "+ incr + "\nCOMPRA: " + str(valorminstr2)+"\nVENTA: " + str(valorminstr) + "\n"
                            print(mensaje)
                            test = telegram_bot_sendtext(mensaje)
                            urllib.request.urlopen(f"https://api.telegram.org/bot5381551675:AAFDvUALkEFHpY0GGB4Cr33BgukyHavwU4Y/sendMessage?chat_id=-1001791296695&text={mensajesocio2}")
                            valor=valorminstr
                            
                    else:
                        if valorminstr >= valor+0.011:
                                
                            incr = str(round(valorminstr -valor,4))
                            
                            mensaje = "ACTUALIZACION!: "+ hora2 +"\nEL DOLAR ONLINE HA SUBIDO S/ "+ incr + "\nCOMPRA: " + str(valorminstr2)+ "\nVENTA: " + str(valorminstr) + "\n"
                            test = telegram_bot_sendtext(mensaje)
                            urllib.request.urlopen(f"https://api.telegram.org/bot5381551675:AAFDvUALkEFHpY0GGB4Cr33BgukyHavwU4Y/sendMessage?chat_id=-1001791296695&text={mensajesocio2}")
                            print(mensaje)
                            valor=valorminstr
        del option2
        del option3
        del listav
        del listac
        t=3600

        time.sleep(t)
        
        auth = tweepy.OAuth1UserHandler("Nx0020RxPlgTj6BSiRuPtXy5z", "sDJLjKxYXsVpC1nidfOeaJAdOB52F2ou6LG4wb3IupqePrdoRj","1527368196595953674-pDBuVvwRd1PZ4CssI8Fs9pqviFB8Tp", "0rMlsyMawwDtP8GsnM45zrXlyXrbquuduPXF0yUDkZdfi")
       
        api = tweepy.API(auth)
        try:
              api.verify_credentials()
              print("Authentication OK")
        except:
              print("Error during authentication")

        # Create API object
        api = tweepy.API(auth, wait_on_rate_limit=True)

        api.update_status("El tipo de cambio Perú se cotiza a:\n\nDolár online S/:\nCompra: "+str(valorminstr2)+"\nVenta: "+str(valorminstr)+"\n\nDólar paralelo S/:\nCompra: "+paraleloc+"\nVenta: "+paralelov+"\nEncuéntranos en Telegram y aprovecha los cupones exclusivos t.me/elcanaldeldolarperu ")

        