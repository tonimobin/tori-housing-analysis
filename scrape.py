from email import header
from bs4 import BeautifulSoup
import requests, string
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from csv import writer

# *** Scrape the first page only, create a new .csv file and write results in it ***
#url = "https://www.tori.fi/koko_suomi/asunnot/vuokrattavat_asunnot?ca=18&cg=1010&st=u&c=1014&w=3&o=1"
#page = requests.get(url)

# soup = BeautifulSoup(page.content, 'html.parser')
# lists = soup.find_all('a', class_="item_row_flex")

# with open('housing.csv', 'w', encoding='utf8', newline='') as f:
#     file_write = writer(f)
#     header = ['Title', 'Price (€/mo)', 'Location']
#     file_write.writerow(header)
#     for list in lists:
#         title = list.find('div', class_="li-title").text.translate(str.maketrans('', '', string.punctuation))
#         price = list.find('p', class_="list_price").text.replace(' €/kk', '')
#         location = list.find('div', attrs={"class":["cat_geo", "cat_geo clean_links"]})
#         location = location.find('p').text
#         info = [title, price, location.strip()]
#         file_write.writerow(info)

# *** Scrape the first <page_num>-1 pages, append results to existing housing.csv file ***
page_num = 1
while page_num != 51:
    url = f"https://www.tori.fi/koko_suomi/asunnot/vuokrattavat_asunnot?ca=18&cg=1010&st=u&c=1014&w=3&o={page_num}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    lists = soup.find_all('a', class_="item_row_flex")
    
    with open('housing.csv', 'a', encoding='utf8', newline='') as f:
        file_write = writer(f)
        if page_num == 1:
            header = ['Title', 'Price (€/mo)', 'Location']
            file_write.writerow(header)
        for list in lists:
            title = list.find('div', class_="li-title").text.translate(str.maketrans('', '', string.punctuation))
            price = list.find('p', class_="list_price").text.replace(' €/kk', '')
            location = list.find('div', attrs={"class":["cat_geo", "cat_geo clean_links"]})
            location = location.find('p').text
            info = [title, price, location.strip()]
            file_write.writerow(info)

    page_num += 1