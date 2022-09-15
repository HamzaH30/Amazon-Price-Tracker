# Imports
import requests
from bs4 import BeautifulSoup
import lxml
import smtplib
import os
from unidecode import unidecode

# Constants
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}
MY_EMAIL = os.environ["MY_EMAIL"]
MY_PASSWORD = os.environ["EMAIL_PASSWORD"]


def send_email(item_name, price):
    with smtplib.SMTP("smtp.mail.yahoo.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=recipient_email,
            msg=f"Subject: AMAZON PRICE ALERT!\n\n{item_name} is now ${price}!\n\nLink to product: {amazon_url}"
        )


# Asking the user the URL of the product they want to track the price of.
amazon_url = input("Enter the URL of the product you want to track the price of: ")

# Asking the user for a price target
price_target = float(input("What is your price target: "))

# Asking the user for their email
recipient_email = input("Please enter your email: ")

# Storing the html code from the amazon website
response = requests.get(amazon_url, headers=HEADERS)
amazon_html = response.text

# Creating BeautifulSoup object, need to use lxml parser instead of html.parser
soup = BeautifulSoup(amazon_html, "lxml")

# Getting the price of the item
price_text = soup.find(name="span", class_="a-offscreen").get_text()
price = float(price_text.split("$")[1])

# Getting the name of the item
item_name = soup.find(name="span", id="productTitle").get_text().strip()
item_name = unidecode(item_name)

# Send email if price is less than $200
if price <= price_target:
    send_email(item_name, price)
