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

    soup = get_soup(base_url)
    submenus = soup.find_all('div', class_='submenu-wrapper level0')
    menu_items = soup.find('ul', class_ = 'megamenu-items').find_all('li')
    categories = init_categories()
    
    i = 0
    for submenu in submenus:
        if menu_items[i].get('data-submenu') is None:
            i = i + 1
        
        main_category = main_categories[i]
        i = i+1
        
        submenu_cols = submenu.find_all('div', class_='submenu-col')
        if main_category in {"% Promocje", "Outlet do -60%"}:
                submenu_cols = submenu.find_all('div', class_='submenu-col')
                for col in submenu_cols:
                    submenu_name = get_submenu_name(col)
                #    glowne kategorie
                    if submenu_name == "":
                        submenu_name = "Najpopularniejsze " + str(get_pronoun(main_category))
                        categories = get_with_main_subcategory(1, categories, submenu_name, main_category,"") 
                    elif submenu_name == "Polecamy":
                        categories = get_with_main_subcategory(1, categories, submenu_name + " " + str(get_pronoun(main_category)), main_category,"")
                    else:
                        categories = get_with_main_subcategory(1, categories, submenu_name, main_category,"")

                    for sub_cat in col.find_all('li'):
                        if submenu_name == "Polecamy":
                            categories = get_with_main_subcategory(1, categories, sub_cat.a.text, submenu_name + " " + str(get_pronoun(main_category)),"")
                        else:
                            categories = get_with_main_subcategory(1, categories, sub_cat.a.text, submenu_name,"")
        else:
            for col in submenu_cols:
                submenu_name = get_submenu_name(col)
        
                if submenu_name not in {"Polecamy", "Najpopularniejsze", " ", ""}:
                    if col.find(text = "Wszystkie") is None and col.find(text = "Wszystkie produkty") is None:
                         top_category = get_submenu_name(col).replace("/","\\")
                         categories = get_with_main_subcategory(1, categories, top_category, main_category,"")
                         for e in col.find_all('li'): 
                            categories = get_with_main_subcategory(1, categories, e.a.text, top_category,"")    
                         continue
                    try:
                        endpoint_name = col.find(text = "Wszystkie").findParent('a').get('href')
                    except:
                        endpoint_name = col.find(text = "Wszystkie produkty").findParent('a').get('href')
                    soup = get_soup("https://8a.pl"+str(endpoint_name))
                    try:
                        description = get_description(soup)
                    except:
                        description = ""
                else:
                    break
                # glowne kategorie
                if submenu_name == "":
                    submenu_name = "Najpopularniejsze " + str(get_pronoun(main_category))
                    categories = get_with_main_subcategory(1, categories, submenu_name, main_category, "") 
                elif submenu_name == "Polecamy":
                    categories = get_with_main_subcategory(1, categories, submenu_name + " " + str(get_pronoun(main_category)), main_category, "")
                else:
                    if(main_category == "Dziecko"):
                        if submenu_name in {"Odzież", "Buty"}:
                            submenu_name = get_children_category(submenu_name)
                    categories = get_with_main_subcategory(1, categories, submenu_name, main_category, description)
                                
                if submenu_name not in {"Polecamy", "Najpopularniejsze", " ", ""}:

                    for type_of_category in soup.find('ul', class_ =  "am-filter-items-attr_category_ids").find_all('li', recursive=False):

                        submenu_elements = type_of_category.find_all('li')
                        flag = 0
                        is_nested = False
                        # print(type_of_category.get('data-label'))
                        for element in submenu_elements:
                            is_nested = True
                            parent_category = element.findParent('li').get('data-label')
                            category = element.get('data-label')
                            # print(main_category)
                            if(main_category == "Dziecko"):
                                if submenu_name in {"Odzież", "Buty"}:
                                    submenu_name = get_children_category(submenu_name)
                            if flag == 0:
                                categories = get_with_main_subcategory(1, categories, parent_category, submenu_name, "") #podkategoria menu
                            flag = 1
                            # if(parent_category == "Rower"):
                            # print(category)
                            categories = get_with_main_subcategory(0, categories, category, parent_category, "") #kategoria z listy
                        if not is_nested:
                            categories = get_with_main_subcategory(1, categories, type_of_category.get('data-label'), submenu_name, "")      
    save_data_to_csv(categories, csv_filename)



def init_categories():
    parent_category = "Home"
    elements = []
    elements.append(["Active (0/1)","Name *","Parent Category", "Root Category (0/1)", "Description"])
    for category in main_categories:
        elements.append([1, category, parent_category, 0,""])
    return elements

def get_submenu_name(col):
    # submenu_name = "" if col.h3 is None else get_content(col.h3)
    submenu_name = get_content(col.h3)
    submenu_name = get_content(col.strong) if submenu_name == "" else submenu_name
    return submenu_name

def get_with_main_subcategory(active, elements, category, parent_category, description):
    elements.append([active, category.replace('/','\\'), parent_category.replace('/','\\'), 0, description])
    return elements

def get_description(soup):
    description = soup.find('div', class_ = 'category-description')
    description = description.find('div').text
    return str(description).strip()