
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


valor=100

#####BUSQUEDA DE DATOS

homeurl = "https://cuantoestaeldolar.pe/"

while((hora.hour) in range (13,20)): #hora horario UTC


    for i in range(8):
        option2=[]
        option3=[]

        page = requests.get(homeurl,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"})
        html_soup1n = BeautifulSoup(page.content,'html.parser')

        #matriz compra (3 primeros paralelo)
        elemento = html_soup1n.find_all('div', class_= "block pl-[8px]") 
        for var in elemento:
                new = var.find('p', class_="ValueQuotation_text___mR_0")
                if new:
                                option2.append(new.text)

                else:    option2.append('')

        #matriz venta (3 primeros paralelo)
        elemento = html_soup1n.find_all('div', class_= "block pl-[10px]") 
        for var in elemento:
                new = var.find('p', class_="ValueQuotation_text___mR_0")
                if new:
                                option3.append(new.text)

                else:    option3.append('')

        #matriz nombre      
        #elemento = html_soup1n.find_all('div', class_= "w-[90px] md:w-36 h-auto flex align-middle justify-center") 
        #for var in elemento:   
        #str_match = re.findall(r'(\w*)(.svg)',str(elemento))
        #print(str_match)
        #for i in range (22):
        #  print(str_match[4+6*i])   


        ##################ORDENAMIENTO
        option2.pop(0)
        option2.pop(0)
        option2.pop(0)
        listac=sorted(option2[0:24])
        
  
        option3.pop(0)
        option3.pop(0)
        option3.pop(0)
        listav=sorted(option3[0:24])
        ########################################LOGICA DE ENVIO

        """def telegram_bot_sendtext(bot_message):
                    bot_token = '5381551675:AAFDvUALkEFHpY0GGB4Cr33BgukyHavwU4Y'
                    bot_chatID = '-1001791296695'
                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                    response = requests.get(send_text)
                    return response.json()
        """
        valorminstr=float(listav[0])
        valorminstr2=float(listac.pop())
        mensajesocio2= urllib.parse.quote_plus("Aprovecha la oferta! Cambia tus dólares en inkamoney.com con el cupón INKADOLAR y obtén un mejor tipo de cambio\nVálido hasta el 31/09/2022")



        if valor == 100:
                
                    mensaje = "HOY: "+dia1+" - EL DOLAR ONLINE SE COTIZA A:\n\nCOMPRA: " + str(valorminstr2)+"\nVENTA: " + str(valorminstr) + "\n\n"
                    #test = telegram_bot_sendtext(f'```{mensaje}```' + "\n")
                    urllib.request.urlopen(f"https://api.telegram.org/bot5381551675:AAFDvUALkEFHpY0GGB4Cr33BgukyHavwU4Y/sendMessage?chat_id=-1001791296695&text={mensajesocio2}")
                    valor=valorminstr
                    print(mensaje)
        else:
                    #0.003 para evitar avisos por cambios muy pequeños de precio  
                    if valorminstr <= valor-0.011:
                            
                            incr = str(round(valor - valorminstr,4))

                            mensaje = "ACTUALIZACION!\nEL DOLAR ONLINE HA BAJADO S/ "+ incr + "\nCOMPRA: " + str(valorminstr2)+"\nVENTA: " + str(valorminstr) + "\n"
                            print(mensaje)
                            #test = telegram_bot_sendtext(mensaje)
                            urllib.request.urlopen(f"https://api.telegram.org/bot5381551675:AAFDvUALkEFHpY0GGB4Cr33BgukyHavwU4Y/sendMessage?chat_id=-1001791296695&text={mensajesocio2}")
                            valor=valorminstr
                            
                    else:
                        if valorminstr >= valor+0.011:
                                
                            incr = str(round(valorminstr -valor,4))
                            
                            mensaje = "ACTUALIZACION!\nEL DOLAR ONLINE HA SUBIDO S/ "+ incr + "\nCOMPRA: " + str(valorminstr2)+ "\nVENTA: " + str(valorminstr) + "\n"
                            #test = telegram_bot_sendtext(mensaje + "\nHora: "+ hora2)
                            urllib.request.urlopen(f"https://api.telegram.org/bot5381551675:AAFDvUALkEFHpY0GGB4Cr33BgukyHavwU4Y/sendMessage?chat_id=-1001791296695&text={mensajesocio2}")
                            print(mensaje)
                            valor=valorminstr
        del option2
        del option3
        del listav
        del listac
        t=3600
        time.sleep(t)

