import os
import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
from time import sleep
import mysql_connector as msc

responses = []

def read_excel():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    loc = (os.path.join(dir_path ,"AmazonScraping.xlsx"))
    df = pd.read_excel(loc)
    nrows = df.shape[0]
    global responses

    for row in range(1,nrows):
        country = df["country"][row]
        asin =df["Asin"][row]
        if isinstance(asin,float):
            asin = str(int(asin))
        data = scrap(country , asin)
        if data is not None:
            responses.append(data)
        sleep(1.5)

def scrap(country,asin):
    HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
    'Accept-Language': 'en-US, en;q=0.5'
}
    url = f"https://www.amazon.{country}/dp/{asin}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 404:
            print("skipping...  ",url)
            return None
    try:
        soup = BeautifulSoup(r.content, "html.parser")
        pretty_soup = BeautifulSoup(soup.prettify(), "html.parser")
        try:
            title = pretty_soup.find(id='productTitle').get_text()
        except AttributeError:
            pass
        try:
            price = pretty_soup.find('span', {'class': 'a-price-whole'}).text
        except AttributeError:
            pass
        try:
            image_url = pretty_soup.find(id= "landingImage")['src']
        except AttributeError:
            pass
        try:
            product_details = pretty_soup.find(id='feature-bullets').get_text()
        except AttributeError:
            pass
        data = {}
        data['title'] = title.strip()
        data['price'] = price.replace('\n',"").replace('.',"").strip()
        data['image_url'] = image_url.strip()
        data['product_details'] = " ".join(product_details.replace('\n',"").split())
        return data
    except Exception as e:
        print(e)

if __name__ == "__main__":
    read_excel()
    with open("responses.json", "w") as outfile:
        json.dump(responses, outfile, indent=1)
    db,cursor = msc.set_connection()
    msc.add_value(db,cursor,responses)

