import csv

from bs4 import BeautifulSoup
import requests
from utils import *
import random

def create_combos(categories):
    filename = "combos.csv"
    data = []
    data.append(["Product ID*", "Attribute (Name:Type:Position)", "Value (Value:Position)", "Quantity"])
    values1 = ["Czerwony:0","Zielony:0","Niebieski:0","Szary:0", "Czarny:0"]
    values2 = ["39:1", "40:1", "41:1", "42:1", "43:1"]
    for category in categories:
        with open('data/'+category+'.csv', 'r', encoding="utf8") as f:
            reader = csv.reader(f, delimiter=";")
            for i, line in enumerate(reader):
                if line[3].lower().find("buty") != -1:
                    id = line[0]
                    attribute1 = "Kolor:color:0"
                    attribute2 = "Rozmiar:select:1"
                    for value1 in values1:
                        for value2 in values2:
                            data.append([id, attribute1+", "+attribute2, value1+", "+value2, random.randint(0, 20)])




    save_data_to_csv(data, filename)