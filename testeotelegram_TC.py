import requests

def telegram_bot_sendtext(bot_message):
              bot_token = '5381551675:AAFDvUALkEFHpY0GGB4Cr33BgukyHavwU4Y'
              bot_chatID = '-1001791296695'
              send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
              response = requests.get(send_text)
              return response.json()

mensaje = "Inflación USA CPI: La inflación en término interanual sube al 8,5%, por debajo del 9,1% de junio y del 8,7% esperado, lo que confirma la ralentización en el ascenso de los precios. Fuente:Investing.com"
#mensaje2="PREVIO=3.92\nRANGO 52 SEMANAS=3.62-4.13\nCAMBIO 5 DIAS=0.18%\nESTOCASTICO %K=65.1\nReferencia diaria: Un valor estocástico %K cercano o mayor a 80 indicaría vender y cercano o menor a 20 indicaría comprar"
test = telegram_bot_sendtext(f'`{mensaje}`')