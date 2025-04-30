import requests
from bs4 import BeautifulSoup
import telegram

TOKEN = '7932524168:AAErHX07Y49MvRMmGgRjRorlS3Jz2jjZx14'
CHAT_ID = '5078979589'

bot = telegram.Bot(token=TOKEN)

siteurl = "https://books.toscrape.com/catalogue/page-"
page = 1
books_list = []

while True:
    url = f"{siteurl}{page}.html"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Səhifə {page} tapılmadı, scraping tamamlandı.")
        break

    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.find_all('h3')
    prices = soup.find_all('p', class_='price_color')
    ratings = soup.find_all('p', class_='star-rating')

    
    for title, price, rating in zip(titles, prices, ratings):
        book_title = title.find('a').get('title')
        book_price = price.get_text()
        book_rating = rating.get('class')[1]

        if book_rating == 'five':
            books_list.append((book_title, book_price))

    page += 1

books_list.sort(key=lambda x: x[1], reverse=True)

message = "Ən Yüksək Reytinqli 5 Kitab:\n\n"

for i, (title, price) in enumerate(books_list[:5], 1):
    message += f"{i}. {title} - {price}\n"

bot.send_message(chat_id=CHAT_ID, text=message)
