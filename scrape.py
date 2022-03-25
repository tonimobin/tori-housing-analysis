from bs4 import BeautifulSoup
import requests 

url = "https://www.tori.fi/uusimaa/asunnot/vuokrattavat_asunnot?ca=18&cg=1010&st=u&c=1014&m=313&w=118"
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')
lists = soup.find_all('section', class_="item_row_flex")

for list in lists:
    title = list.find('a', class_="")
    price = list.find('a', class_="")
    apt_type = list.find('a', class_="")
    year = list.find('a', class_="")