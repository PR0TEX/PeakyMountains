from bs4 import BeautifulSoup
import requests
import pandas as pd

option = 'ona'
base_url = 'https://8a.pl/'
paging = '?p='
page = 1
elements = []
run = True
link_to_scrap = base_url + option + paging
csv_filename = option + '.csv'

while run:
    site = requests.get(link_to_scrap + str(page)).text
    soup = BeautifulSoup(site, 'lxml')
    items = soup.find_all('div', class_='product-item-info')
    if len(items) == 0:
        run = False
    for item in items:
        discount_item = item.find('div', class_='button-product-label type-discount')
        discount = discount_item.text if discount_item else ""
        type_new_item = item.find('div', class_='button-product-label type-new')
        type_new = type_new_item.text if type_new_item else ""
        image_item = item.find('img', class_='product-image-photo')
        image_url = image_item.get('src') if image_item else ""
        title_item = item.find('a', class_='product-item-link')
        title = title_item.text if title_item else ""
        special_price_span = item.find('span', class_='special-price')
        special_price_item = special_price_span.find('span', class_='price') if special_price_span else False
        special_price = special_price_item.text if special_price_item else ""
        old_price_span = item.find('span', class_='price-container price-final_price tax weee')
        old_price_item = old_price_span.find('span', class_='price') if old_price_span else False
        old_price = old_price_item.text if old_price_item else ""
        element = {
            'discount': {discount},
            'type': {type_new},
            'image_url': {image_url},
            'title': {str(title).strip()},
            'special_price': {special_price},
            'old_price': {old_price}
        }
        elements.append(element)
    page = page + 1

df = pd.DataFrame(elements)
df.to_csv(csv_filename)

