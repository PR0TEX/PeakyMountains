from categories import scrap_categories_to_csv
from product import scrap_products_depending_on_category
from combo import create_combos
from utils import connect_csv

product_id = 0
categories = ["on", "ona", "dziecko", "turystyka", "wspinanie", "bieganie", "rower", "skitouring", "outlet", "promocja"]
# categories = ["bieganie", "rower", "skitouring", "outlet", "promocja"]

# scrap_categories_to_csv()
# for category in categories:
#     product_id = scrap_products_depending_on_category(category, product_id)

create_combos(categories)
 
# connect_csv()