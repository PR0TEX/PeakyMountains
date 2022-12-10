import pandas as pd
import os

def get_content(content):
    return content.text if content else ""

def create_link_with_query_param(base_url, page_category, query_param, param_value):
    return base_url + page_category + "?" + query_param + "=" + param_value

def save_data_to_csv(data, filename):
    output_directory = "./data/"
    df = pd.DataFrame(data)

    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    df.to_csv("./data/" + filename, header=False, index=False, sep=";")
    print("Data saved to file "+filename)

