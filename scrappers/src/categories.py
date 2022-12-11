from bs4 import BeautifulSoup
import requests
from utils import *

def get_categories():
    site = requests.get(base_url).text
    soup = BeautifulSoup(site, 'lxml')
    categories = soup.find_all('li', class_='level0')
    elements = []
    for category in categories:
        category_name = get_content(category.span)
        elements.append(category_name)

    return elements


main_categories = get_categories()


def scrap_categories_to_csv():
    csv_filename = "categories.csv"

    soup = get_page_soup(base_url)
    submenus = soup.find_all('div', class_='submenu-wrapper level0')
    menu_items = soup.find('ul', class_ = 'megamenu-items')
    categories = init_categories()
    for submenu in submenus:
        # print(submenu)
        id_category = submenus.index(submenu)
        main_category = main_categories[id_category]
        if()
        # if main_category == "Nowości":
        #     print("NOOOOOOOOWE")
                
        # try:
        submenu_cols = submenu.find_all('div', class_='submenu-col')
            # submenu_cols.find('li')
        # except:
        #     print("OOOOPS")
        #     continue
        print(main_category)
        for col in submenu_cols:
            submenu_name = get_submenu_name(col)
            if submenu_name not in {"Polecamy", "Najpopularniejsze", " ", ""}:
                # print(get_url_without_accents(get_product_url(submenu_name)))
                # print(submenu_name)
                # print("NAZWA " + submenu_name)
                if col.find(text = "Wszystkie") is None:
                    continue    
                
                endpoint_name = col.find(text = "Wszystkie").findParent('a').get('href')
                print(endpoint_name)
                soup = get_page_soup("https://8a.pl"+str(endpoint_name))   #nazwa_do_zmiany     
                print("https://8a.pl"+str(endpoint_name))
                description = get_description(soup)
            else:
                # print("EWAKUACJA")
                break
            
            if submenu_name == "":
                submenu_name = "Najpopularniejsze " + str(get_pronoun(main_category))
                categories = get_with_main_subcategory(categories, submenu_name, main_category) 
            elif submenu_name == "Polecamy":
                categories = get_with_main_subcategory(categories, submenu_name + " " + str(get_pronoun(main_category)), main_category)
            else:
                categories = get_with_main_subcategory(categories, submenu_name, main_category)
                              
            if submenu_name not in {"Polecamy", "Najpopularniejsze", " ", ""}:
                
                # submenu_elements = soup.find('form', {"data-amshopby-filter": "attr_category_ids"}).find(recursive=False)
                # ="
                # print()
                for x in soup.find('ul', class_ =  "am-filter-items-attr_category_ids").find_all('li'):
                    
                    # submenu_elements = soup.find('ul', {"class": "items-children"}).find_all('li')
                    try:
                        submenu_elements = x.find_all('li')
                    
                        for element in submenu_elements:
                            parent_category = element.findParent('li').get('data-label')
                            category = element.get('data-label')
                            # print(category)
                    except:
                        parent_category = x.findParent('li').get('data-label')
                        category = x.get('data-label')
                        
                #     if submenu_name == "Polecamy":
                #         categories.append([1, sub_category,submenu_name + " " + str(get_pronoun(main_category)), 0])    
                #     else:
                #         categories.append([1, sub_category, submenu_name, 0])
        # soup = get_page_soup(base_url)
    save_data_to_csv(categories, csv_filename)



def init_categories():
    parent_category = "Home"
    elements = []
    elements.append(["Active (0/1)","Name *","Parent Category", "Root Category (0/1)"])
    for category in main_categories:
        elements.append([1, category, parent_category, 0])
    return elements

def get_submenu_name(col):
    submenu_name = get_content(col.h3)
    submenu_name = get_content(col.strong) if submenu_name == "" else submenu_name
    return submenu_name

def get_with_main_subcategory(elements, category, parent_category):
    elements.append([1, category, parent_category, 0])
    return elements

def get_description(soup):
    description = soup.find('div', class_ = 'category-description')
    description = description.find('div').text
    return description