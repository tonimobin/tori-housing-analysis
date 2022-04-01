from email import header
from bs4 import BeautifulSoup
import requests, string
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from csv import writer
import re 
# *** Scrape the first <page_num>-1 pages, append results to existing housing.csv file ***
page_num = 1
while page_num != 4:
    url = f"https://www.tori.fi/koko_suomi/asunnot/myytavat_asunnot?ca=18&cg=1010&c=1012&w=3&o={page_num}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    lists = soup.find_all('a', class_="item_row_flex")
    
    with open('housing.csv', 'a', encoding='utf8', newline='') as f:
        file_write = writer(f)
        if page_num == 1:
            header = ['Title', 'Price', 'Size', 'Type', 'Year', 'Location']
            file_write.writerow(header)
        for list in lists:
            title = list.find('div', class_="li-title").text.translate(str.maketrans('', '', string.punctuation))
            price = list.find('p', class_="list_price").text.replace(' €', '').replace(" ", "")

            location = list.find('div', attrs={"class":["cat_geo", "cat_geo clean_links"]})
            location = location.find('p').text 

            # Contains the parse that has info about size, house_type and year
            list_container = list.find('div', attrs={"class":["list-details-container"]})
            list_container = str(list_container.find('p', attrs={"class":["param"]}))

            size = list_container[list_container.find(">")+1:list_container.find('m²')+2]
            house_type = ""
            house_types = ["Rivitalo", "Kerrostalo", "Omakotitalo", "Luhtitalo"]
            for w in house_types:
                if w in list_container:
                    house_type = w

            year = ""
            year_parse = re.findall(r'\d{4}', list_container)
            if len(year_parse) > 0:
                year = year_parse[0]

            info = [title, price, size, house_type, year, location.strip()]
            file_write.writerow(info)
            
    page_num += 1