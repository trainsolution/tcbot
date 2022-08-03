import requests

def telegram_bot_sendtext(bot_message):
              bot_token = '5381551675:AAFDvUALkEFHpY0GGB4Cr33BgukyHavwU4Y'
              bot_chatID = '-1001791296695'
              send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
              response = requests.get(send_text)
              return response.json()

mensaje = "DATOS DIARIOS REFERENCIALES\nPREVIO = 3.91\nRANGO 52 SEM = 3.62-4.13\nCAMBIO 5 DIAS  =  0.24%\nESTOCASTICO %K = 55.35\nReferencia diaria: un valor estocástico %K cercano a 80 indicaría vender y cercano a 20 indicaría comprar"
test = telegram_bot_sendtext(f'`{mensaje}`')