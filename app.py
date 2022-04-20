from unittest import result
from bs4 import BeautifulSoup
import requests
import schedule
import time
import urllib.request
import pandas as pd


def bot_send_text(bot_message):
    
    bot_token = '5231406261:AAE1lr7A9feeiv9Ejt3awEyigwzpxtyoqRo'
    bot_chatID = '-796627951'
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
    
    string="A ocurrido un sismo en las cercanías de iquique" "\n"
    for column in dataset_filter.head(1).columns:
        string += column + " : " + str(dataset_filter[column].values[0]) + "\n"
    
    return string



def report():
    sismo= f'{sismo_scraping()}'
    bot_send_text(sismo)


if __name__ == '__main__':
        
    # schedule.every().day.at("12:34").do(report)
    # schedule.every(1).hours.do(report)

    while True:
        schedule.run_pending()
        time.sleep(1)
