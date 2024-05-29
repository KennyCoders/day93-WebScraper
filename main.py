import requests
from bs4 import BeautifulSoup
import csv
import re

# URL of the Steam top sellers page
URL = "https://store.steampowered.com/search/?filter=topsellers"

# Get HTML content
response = requests.get(URL)
steam_page = response.text

# Soup It up
soup = BeautifulSoup(steam_page, "html.parser")

# Find games based on HTML element
elements = soup.find_all('a', class_='search_result_row ds_collapse_flag')


# Lists for CSV file
titles = []
ratings = []
prices = []
release_dates = []

# Extract information for each game
for element in elements:
    # Title
    title = element.find('span', class_='title').text.strip() if element.find('span', class_='title') else 'N/A'
    titles.append(title)

    # Release Date
    release_date = element.find('div', class_='col search_released responsive_secondrow').text.strip() if element.find(
        'div', class_='col search_released responsive_secondrow') else 'N/A'
    release_dates.append(release_date)

    # Rating
    rating_span = element.find('span', class_='search_review_summary')
    rating = rating_span['data-tooltip-html'] if rating_span and 'data-tooltip-html' in rating_span.attrs else 'N/A'
    rating = re.sub('<br>', ', ', rating)  # Remove the <br> tag using re.sub
    ratings.append(rating)

    # Price
    price_div = element.find('div', class_='discount_final_price')
    price = price_div.text.strip() if price_div else 'N/A'
    prices.append(price)

with open('steam_games.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Title', 'Rating', 'Price', 'Release Date'])  # Header
    for data in zip(titles, ratings, prices, release_dates):
        writer.writerow(data)

print("CSV file has been created successfully homie!")
