import requests
import urllib

def telegram_bot_sendtext(bot_message):
                bot_token = '5381551675:AAFDvUALkEFHpY0GGB4Cr33BgukyHavwU4Y'
                bot_chatID = '-1001791296695'
                send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                response = requests.get(send_text)
                return response.json()


mensaje = urllib.parse.quote_plus("¡Amigos tenemos una gran noticia!\nAhora toda la comunidad del Canal del Dólar Perú podrá disfrutar del cupón INKADOLAR para comprar o vender dólares desde la web de INKAMONEY (inkamoney.com), con el que obtendrás un beneficio adicional en el tipo de cambio.\nVálido hasta el 31/08/2022")
#test = telegram_bot_sendtext(f'`{mensaje}`' + "\n")
 
urllib.request.urlopen(f"https://api.telegram.org/bot5381551675:AAFDvUALkEFHpY0GGB4Cr33BgukyHavwU4Y/sendMessage?chat_id=-1001791296695&text={mensaje}")