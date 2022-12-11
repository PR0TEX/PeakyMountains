from bs4 import BeautifulSoup
import requests
from utils import *


def scrap_products_depending_on_category(page_category):
    page = 1
    elements = []
    run = True
    csv_filename = page_category + '.csv'
    elements.append(["Active (0/1)","Name *", "Categories (x,y,z)", "Price tax included", "On sale(0/1)", "Discount percent", "Description", "Image URLs"])
    
    while run:
        link_to_scrap = create_link_with_query_param(base_url, page_category, query_param, str(page))
        soup = get_soup(link_to_scrap)
        items = soup.find_all('div', class_='product-item-info')
        if page == 2:
            run = False
        for item in items:
            soup = get_soup(link_to_scrap)
            
            discount_item = item.find('div', class_='button-product-label type-discount')
            discount = get_content(discount_item)[1:-1]
           
            title_item = item.find('a', class_='product-item-link')
            title = str(get_content(title_item)).strip()
            
            product_url = title_item.get('href')
            
            soup = get_soup(product_url)

            image_urls = get_photos(soup)
            image_urls = (','.join(image_urls))
            
            description = get_description(soup)
            
            if get_product_name(product_url) != "":
                size_charts = get_size(get_product_name(product_url))
            else:
                size_charts = ""
            
            categories = get_category_tree(soup)
                
            special_price_span = item.find('span', class_='special-price')
            special_price_item = special_price_span.find('span', class_='price') if special_price_span else False
            special_price = get_content(special_price_item)
            
            on_sale = 1 if special_price != "" else 0
            
            old_price_span = item.find('span', class_='price-container price-final_price tax weee')
            old_price_item = old_price_span.find('span', class_='price') if old_price_span else False
            old_price = get_content(old_price_item)
            old_price = old_price[:-3].replace(',','.')
            
            elements.append([1, title, categories, old_price, on_sale, discount, description, image_urls])
        
        page = page + 1

    save_data_to_csv(elements, csv_filename)
    

def get_photos(soup):
    photos_img = soup.find_all('img', class_ = 'sm-fancy-gallery__item-image')
    photos_urls = []
    for photo in photos_img:
        photos_urls.append(photo.get('src'))
    return photos_urls

def get_description(soup):
    description_div = soup.find('div', class_ ="value")
    description_paragraphs = description_div.find_all('p')
    description = ""
    
    for paragraph in description_paragraphs:
        description += paragraph.text + "\n"   
    
    description += "\n" + description_div.h2.text + "\n"    
    
    for feature in description_div.ul.find_all('li'):
        description += "\t" + feature.text + "\n"
        
    return description

def get_category_tree(soup):
    categories = soup.find('div', class_="breadcrumbs")
    category = ""
    category_number = 0

    for cat_part in categories.find_all('li'):
        if str(cat_part.text).strip() == "Strona główna":
            category += "Home" + ","
        elif category_number == len(categories.find_all('li')) - 1:
            break
        else:
            category += str(cat_part.text).strip() + ","
        category_number = category_number + 1
    return category[:-1]
    