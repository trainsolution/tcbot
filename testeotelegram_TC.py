import requests
import urllib

mensajea = "EL DOLAR SE COTIZA A:\nPARALELO COMPRA \nPARELELO VENTA:   +  \n\n     - TC CASAS DE CAMBIO ONLINE -    "
 
def telegram_bot_sendtext(bot_message):
              bot_token = '5381551675:AAFDvUALkEFHpY0GGB4Cr33BgukyHavwU4Y'
              bot_chatID = '811650091'
              send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
              response = requests.get(send_text)
              return response.json()
mensajesocio1= "Aprovecha la oferta de INKAMONEY ingresando el cupón INKADOLAR \n(Válido hasta el 31/09/2022)"
mensajesocio2= urllib.parse.quote_plus("Aprovecha la oferta! Cambias tus dólares en inkamoney.com con el cupón INKADOLAR y obtén un mejor tipo de cambio\n(Válido hasta el 31/09/2022)")


mensaje = "Inflación USA CPI: La inflación en término interanual sube al 8,5%, por debajo del 9,1% de junio y del 8,7% esperado, lo que confirma la ralentización en el ascenso de los precios. Fuente:Investing.com"
#mensaje2="PREVIO=3.92\nRANGO 52 SEMANAS=3.62-4.13\nCAMBIO 5 DIAS=0.18%\nESTOCASTICO %K=65.1\nReferencia diaria: Un valor estocástico %K cercano o mayor a 80 indicaría vender y cercano o menor a 20 indicaría comprar"
#test = telegram_bot_sendtext(f'`{mensajesocio1}`')
#test = telegram_bot_sendtext(mensajesocio1)

mensaje2 = urllib.parse.quote_plus("¡Amigos tenemos una gran noticia!\nAhora toda la comunidad del Canal del Dólar Perú podrá disfrutar del cupón INKADOLAR para comprar o vender dólares desde la web de INKAMONEY (inkamoney.com), con el que obtendrás un beneficio adicional en el tipo de cambio.\nVálido hasta el 31/08/2022")
test = telegram_bot_sendtext(mensajea + "\n")

urllib.request.urlopen(f"https://api.telegram.org/bot5381551675:AAFDvUALkEFHpY0GGB4Cr33BgukyHavwU4Y/sendMessage?chat_id=811650091&text={mensajesocio2}")