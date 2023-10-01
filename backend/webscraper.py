import requests
from bs4 import BeautifulSoup
import re
import sqlite3

# Function to scrape fighter details
def scrape_fighter_details(fighter_name):
    # Split the fighter name by whitespace
    fighter_name = fighter_name.lower()
    name_parts = fighter_name.split()
    # Join the name parts with hyphens
    name_hyphenated = "-".join(name_parts)

    url = f"https://www.ufc.com/athlete/{name_hyphenated}"
    # Fetch the page content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the fighter image
    image_div = soup.find("div", class_="hero-profile__image-wrap")
    if image_div:
        img_tag = image_div.find("img")
        if img_tag and 'src' in img_tag.attrs:
            img_url = img_tag['src']
            return {"image_url": img_url}
    return {"image_url": None}

# Scrape data
# fighter_url = "http://ufcstats.com/fighter-details/f4c49976c75c5ab2"
# scraped_data = scrape_fighter_details("Jon Jones")

# print(scraped_data)