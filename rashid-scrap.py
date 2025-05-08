import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook


# Telegram konfiqurasiyası
BOT_TOKEN = ""
CHAT_ID = ""  # DÜZGÜN chat ID budur!



# Telegram-a mesaj göndərən funksiya
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("✅ Telegram mesajı göndərildi!")
    else:
        print("❌ Telegram mesaj göndərilə bilmədi:", response.text)



# Define URL (BMW listings)
url = "https://books.toscrape.com/catalogue/page-2.html"

# Request page
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Prepare Excel
wb = Workbook()
ws = wb.active
ws.title = "BMW Listings"
ws.append(["Title", "Price", "Datetime","Attributes"])

# Scrape listings
cars = soup.find_all("article", class_="product_pod")

for car in cars:
    title_tag = car.find("h3")
    price_tag = car.find("div", class_="product-price")
    datetime_tag = car.find("div", class_="products-i__datetime")    
    attribute_tag = car.find("div", class_="products-i__attributes")
    print(title_tag.get_text())

    title = title_tag.get_text(strip=True) if title_tag else ""
    price = price_tag.get_text(strip=True) if price_tag else ""    
    datetime = datetime_tag.get_text(strip=True) if datetime_tag else ""    
    attribute = attribute_tag.get_text(strip=True) if attribute_tag else ""
    
    send_telegram_message(title)
    
    if title and price and datetime and attribute:
        ws.append([title, price,datetime,attribute])

# Save Excel

wb.save("bmw_listings.xlsx")
print("Done: bmw_listings.xlsx")
