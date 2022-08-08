import requests

def telegram_bot_sendtext(bot_message):
              bot_token = '5381551675:AAFDvUALkEFHpY0GGB4Cr33BgukyHavwU4Y'
              bot_chatID = '-1001791296695'
              send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
              response = requests.get(send_text)
              return response.json()

mensaje = " El dólar sube tras datos económicos en EEUU: El índice del dólar estadounidense subía el miércoles después de que datos mostraron un sorprendente repunte del sector de servicios de Estados Unidos en julio, lo que dio a la divisa un mayor apoyo tras comentarios de autoridades de la Reserva Federal del martes. Fuente:Investing.com"
mensaje2="PREVIO=3.92\nRANGO 52 SEMANAS=3.62-4.13\nCAMBIO 5 DIAS=0.18%\nESTOCASTICO %K=65.1\nReferencia diaria: Un valor estocástico %K cercano o mayor a 80 indicaría vender y cercano o menor a 20 indicaría comprar"
test = telegram_bot_sendtext(f'`{mensaje2}`')