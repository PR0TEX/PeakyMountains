import pandas as pd

def get_content(content):
    return content.text if content else ""

def create_link_with_query_param(base_url, page_category, query_param, param_value):
    return base_url + page_category + "?" + query_param + "=" + param_value

def save_data_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv("./data/" + filename)
    print("Data saved to file "+filename)
