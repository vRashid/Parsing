import requests
from bs4 import BeautifulSoup

siteurl = "https://books.toscrape.com/catalogue/page-"
page = 1

while True:
    url = f"{siteurl}{page}.html"
    response = requests.get(url)
    
    if response.status_code != 200:
        break  

    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.find_all('h3')
    prices = soup.find_all('p', class_='price_color')

    for title, price in zip(titles, prices):
        print(f"Kitab Başlığı: {title.find('a').get('title')}")
        print(f"Qiymət: {price.get_text()}\n")
    
    page += 1
