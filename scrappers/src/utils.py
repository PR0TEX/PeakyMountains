import pandas as pd
import os
from unidecode import unidecode
from bs4 import BeautifulSoup
import requests

pronouns = {
    "On": "dla niego",
    "Ona": "dla niej",
    "Dziecko": "dla dziecka",
    "Turystyka": "do turystyki",
    "Wspinanie i Alipinizm": "do wspinania i aplinizmu",
    "Bieganie": "do biegania",
    "Rower": "do roweru",
    "Skitouring": "do skitouringu",
    "Promocje": "z promocji"
}

sizes = {
    "Kurtka": "S,M,L,XL,XXL",
    "Koszulka": "S,M,L,XL",
    "Koszula": "S,M,XL,XLL",
    "Bluza": "S,M,L,XL",
    "Spodenki": "48,50,52,54",
    "T-Shirt": "XS,S,L,XL",
    "Buty": "41,42,43,44,45,46",
    "Bokserki": "S,M,L,XL",
    "Skarpety": "35-38,39-41,42-44,45-47"
}

base_url = 'https://8a.pl/'
query_param = 'p'


def get_content(content):
    return str(content.text) if content else ""

def create_link_with_query_param(base_url, page_category, query_param, param_value):
    return base_url + page_category + "?" + query_param + "=" + param_value

def save_data_to_csv(data, filename):
    output_directory = "./data/"
    df = pd.DataFrame(data)

    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    df.to_csv("./data/" + filename, header=False, index=False, sep=";")
    print("Data saved to file "+filename)

def get_pronoun(noun):
    return pronouns.get(noun)

def get_size(product):
    return sizes.get(product)

def get_product_name(text):
    if "kurtka" in text:
        return "Kurtka"
    elif "koszulka" in text:
        return "Koszulka"
    elif "koszula" in text:
        return "Koszula"
    elif "bluza" in text:
        return "Bluza"
    elif "spodenki" in text:
        return "Spodenki"
    elif "t-shirt" in text:
        return "T-Shirt"
    elif "buty" in text:
        return "Buty"
    elif "Bokserki" in text:
        return "Bokserki"
    elif "skarpety" in text:
        return "Skarpety"

    return ""

def get_url_without_accents(url):
    return unidecode(url)

def get_product_url(title):
    item_name_elements = title.split(" ")
    item_endpoint = ""
    for element in item_name_elements:
        if element == "-" or element == "–":
            continue
        elif item_endpoint != "" and item_endpoint[-1:] != "-":
            item_endpoint = item_endpoint + "-" + element
        else:
            item_endpoint = item_endpoint + element
        
        item_endpoint = item_endpoint.replace("/", "-")
        item_endpoint = item_endpoint.replace(".", "-")
        
        while(item_endpoint[-1:] == "-"):
            item_endpoint = item_endpoint[:-1]
    
    return (base_url + item_endpoint).lower()

def get_page_soup(url):
    site = requests.get(url).text
    soup = BeautifulSoup(site, 'lxml')
    return soup