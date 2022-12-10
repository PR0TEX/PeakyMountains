from bs4 import BeautifulSoup
import requests
from utils import *

base_url = 'https://8a.pl/'
query_param = 'p'


def get_categories():
    site = requests.get(base_url).text
    soup = BeautifulSoup(site, 'lxml')
    categories = soup.find_all('li', class_='level0')
    elements = []
    for category in categories:
        category_name = get_content(category.span)
        elements.append(category_name)

    return elements


categories = get_categories()


def scrap_products_depending_on_category(page_category):
    page = 1
    elements = []
    run = True
    csv_filename = page_category + '.csv'
    elements.append(["Discount percent", "Nowe", "Image URLs", "Description", "Base price", "Cost price" ])
    while run:
        link_to_scrap = create_link_with_query_param(base_url, page_category, query_param, str(page))
        site = requests.get(link_to_scrap).text
        soup = BeautifulSoup(site, 'lxml')
        items = soup.find_all('div', class_='product-item-info')
        if page == 2:
            run = False
        for item in items:
            discount_item = item.find('div', class_='button-product-label type-discount')
            discount = get_content(discount_item)
            type_new_item = item.find('div', class_='button-product-label type-new')
            type_new = get_content(type_new_item)
            image_item = item.find('img', class_='product-image-photo')
            image_url = image_item.get('src') if image_item else ""
            title_item = item.find('a', class_='product-item-link')
            title = get_content(title_item)
            special_price_span = item.find('span', class_='special-price')
            special_price_item = special_price_span.find('span', class_='price') if special_price_span else False
            special_price = get_content(special_price_item)
            old_price_span = item.find('span', class_='price-container price-final_price tax weee')
            old_price_item = old_price_span.find('span', class_='price') if old_price_span else False
            old_price = get_content(old_price_item)
            elements.append([discount[1:-1], type_new, image_url, str(title).strip(), old_price[:-3].replace(',','.'), special_price[:-3].replace(',','.')])
        page = page + 1

    save_data_to_csv(elements, csv_filename)


def scrap_categories_with_subcategories():
    csv_filename = "subcategories.csv"
    site = requests.get(base_url).text
    soup = BeautifulSoup(site, 'lxml')
    submenus = soup.find_all('div', class_='submenu-wrapper level0')

    for submenu in submenus:
        id_category = submenus.index(submenu)
        main_category = categories[id_category]
        menus = []
        submenu_cols = submenu.find_all('div', class_='submenu-col')
        menus.append(["Parent Category", "Name"])
        for col in submenu_cols:
            submenu_name = get_content(col.h3)
            submenu_name = get_content(col.strong) if submenu_name == "" else submenu_name
            submenu_elements = col.find_all('li')
            elements = ()
            for element in submenu_elements:
                sub_category = get_content(element.a)
                elements = elements + (sub_category,)
            menus.append([submenu_name, elements])
        save_data_to_csv(menus, main_category + "_" + csv_filename)



def scrap_categories():
    csv_filename = "categories.csv"
    elements = []
    elements.append(["Category"])
    for category in categories:
        elements.append(category)
    save_data_to_csv(elements, csv_filename)
    
    
scrap_products_depending_on_category('ona')
scrap_categories_with_subcategories()
scrap_categories()