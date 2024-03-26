from unittest import result
from bs4 import BeautifulSoup
import requests
import schedule
import time
import urllib.request
import pandas as pd


def bot_send_text(bot_message):
    
    bot_token = '******'
    bot_chatID = '*******'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()




def sismo_scraping():
    e = urllib.request.urlopen("http://www.sismologia.cl/ultimos_sismos.html").read()
    soup = BeautifulSoup(e, 'html.parser')

    # Obt    enemos la tabla

    tabla_sismos = soup.find_all('table')[0]

    # Obtenemos todas las filas
    rows = tabla_sismos.find_all("tr")

    output_rows = []
    for row in rows:
        # obtenemos todas las columns
        cells = row.find_all("td")
        output_row = []
        if len(cells) > 0:
            for cell in cells:
                output_row.append(cell.text)
            output_rows.append(output_row)

    dataset = pd.DataFrame(output_rows)

    dataset.columns = [
        "Fecha Local",
        "Fecha UTC",
        "Latitud",
        "Longitud",
        "Profundidad [Km]",
        "Magnitud",
        "Referencia Geográfica",
    ]
    dataset[["Latitud", "Longitud"]] = dataset[["Latitud", "Longitud"]].apply(pd.to_numeric)
    
    dataset_filter = dataset[
            (-21.655 <= dataset["Latitud"])
            & (dataset["Latitud"] <= -19.370)
            & (-72.316 <= dataset["Longitud"])
            & (dataset["Longitud"] <= -68.426)
            ]
    
    string="A ocurrido un sismo en las cercanías de iquique" "\n""\n" "Datos del sismo:" "\n" "\n" #titulo con salto de linea
    
    
    for column in dataset_filter.head(1).columns:
        string += column +  " : " + str(dataset_filter[column].values[0]) + "\n"
    return string
        
def main():
    ultimo_sismo = (None)
    while True:
        text = f'{sismo_scraping()}'
        if (text) != ultimo_sismo:
            bot_send_text(text)
            ultimo_sismo = (text)
        time.sleep(60) 


if __name__ == '__main__':

    main()

