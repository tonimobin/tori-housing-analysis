from bs4 import BeautifulSoup
import requests 

url = "https://www.tori.fi/uusimaa?q=&cg=1010&w=3&st=u&c=1014&ros=&roe=&ss=&se=&ht=&at=&mre=&ca=18&l=0&md=th"
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')
lists = soup.find_all('a', class_="item_row_flex")

for list in lists:
    title = list.find('div', class_="li-title").text
    price = list.find('p', class_="list_price").text
    location = list.find('div', attrs={"class":["cat_geo", "cat_geo clean_links"]})
    location = location.find('p').text
    info = [title, price, location.strip()]
    
    print("info: ", info)