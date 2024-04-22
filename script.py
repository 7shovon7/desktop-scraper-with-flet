# %%
import pandas as pd
import json
import requests
import os
import jinja2
from time import sleep
from random import randint
import cloudscraper
from datetime import datetime, UTC

# %% [markdown]
# # Constants

# %%
SUPPORTED_FILE_EXTENSIONS = [
    'csv',
    'xlsx',
]
reuter_url = "https://www.reuter.com/services/fr-fr/services/products?%24search={code}&%24limit=1&%24populate%5BoptionsCount%5D=1&%24language=fr"
sanitino_url = "https://www.sanitino.fr/fulltext$a949-autocomplete.xml?_infuse=1&query={code}"

# %% [markdown]
# # Functions

# %%
def formatted_current_date():
    return datetime.strftime(datetime.now(UTC), "%d-%m-%Y")


def formatted_current_time():
    return datetime.strftime(datetime.now(UTC), "%d-%m-%Y_%H-%M-%S")


def create_directory(dir_name: str):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    return dir_name


def read_input_data(input_path: str):
    path_extention = input_path.split('.')[-1]
    if path_extention in SUPPORTED_FILE_EXTENSIONS:
        if path_extention == 'csv':
            df = pd.read_csv(input_path)
        elif path_extention == 'xlsx':
            df = pd.read_excel(input_path)
    else:
        print('File format is not supported. Use only one of these - ' + ', '.join(SUPPORTED_FILE_EXTENSIONS))
        df = None
    return df


def convert_price_to_float(price):
    if not (price is None or (type(price) == str and price == '')):
        price_str = str(price)
        try:
            price_str = price_str.replace(',', '')
            price = float(price_str)
        except Exception as e:
            print(e)
    return price


# def get_api_data(url, site, *args, **kwargs):
#     payload = {
#     'source': 'universal',
#     'url': url,
#     'user_agent_type': 'desktop',
#     'context': [
#             {'key': 'http_method', "value": 'get'}
#         ],
#     }
#     # Get response.
#     response = requests.request(
#         'POST',
#         'https://realtime.oxylabs.io/v1/queries',
#         auth=('sanipromo', 'kasA_kd3A090lsdk'), #Your credentials go here
#         json=payload,
#     )
#     try:
#         r = response.json()['results'][0]['content']
#     except Exception as e:
#         print(e)
#         return {}
#     try:
#         if site == 'r':
#             dict_data = json.loads(r)
#         elif site == 's':
#             dict_data = json.loads(r.split('id="luigis-box-Autocomplete">')[1].split('</script>')[0].strip())
#         else:
#             dict_data = r
#     except Exception as e:
#         print(e)
#         dict_data = {}
#     return dict_data
    


def get_api_data(url, site, proxy=None):
    # scraper = cloudscraper.create_scraper()
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )
    should_continue = True
    if proxy:
        r = scraper.get(url, proxies=proxy)
    else:
        while should_continue:
            try:
                r = scraper.get(url)
                should_continue = False
            except ConnectionError:
                print("Connection error happened! Retrying...")
                sleep(5)
    try:
        if site == 'r':
            dict_data = json.loads(r.text)
        elif site == 's':
            dict_data = json.loads(r.text.split('id="luigis-box-Autocomplete">')[1].split('</script>')[0].strip())
        else:
            dict_data = r
    except Exception as e:
        print(e)
        dict_data = {}
    scraper.close()
    return dict_data


# def get_api_data(url, site):
#     proxies = {
#         "https": "scraperapi.autoparse=true.country_code=eu.device_type=desktop:949c64aaa9c50e3362a478698932e6f6@proxy-server.scraperapi.com:8001"
#     }
#     r = requests.get(url, proxies=proxies, verify=False)
#     try:
#         if site == 'r':
#             dict_data = json.loads(r.text)
#         elif site == 's':
#             dict_data = json.loads(r.text.split('id="luigis-box-Autocomplete">')[1].split('</script>')[0].strip())
#         else:
#             dict_data = r
#     except Exception as e:
#         print(e)
#         dict_data = {}
#     return dict_data


# def get_api_data(url):
#     payload = {
#         'api_key': '949c64aaa9c50e3362a478698932e6f6',
#         'url': url,
#         'follow_redirect': False,
#         'autoparse': True,
#         'retry_404': True,
#         'country_code': 'eu',
#         'device_type': 'desktop'
#     }
#     r = requests.get('https://api.scraperapi.com/', params=payload)
#     return r



# def save_json_data(file_name: str, data: dict):
#     with open(file_name, 'w') as f:
#         f.write(json.dumps(data, indent=4))


# def color_price(my_price, reuter, sanitino):
#     my_price = float(my_price)
#     # If both Reuter and Sanitino prices are None, color the cell red
#     if pd.isnull(reuter) and pd.isnull(sanitino):
#         return 'background-color: red'
#     # If either Reuter or Sanitino price is present
#     elif pd.notnull(reuter) or pd.notnull(sanitino):
#         # If my price is the lowest, color the cell green
#         if my_price < reuter and my_price < sanitino:
#             return 'background-color: green'
#         # If my price is the highest, color the cell yellow
#         elif my_price > reuter and my_price > sanitino:
#             return 'background-color: yellow'
#         # If my price is in the middle, color the cell chartreuse (#9ACD32)
#         else:
#             return 'background-color: blue'
#     # If none of the above conditions match, return default style
#     else:
#         return ''


def drop_unnecessary_columns(input_df: pd.DataFrame):
    all_columns = list(input_df.columns)
    allowed_columns = ['Code', 'Price', 'Reuter', 'Sanitino']
    columns_to_be_dropped = [col for col in all_columns if col not in allowed_columns]
    input_df_m = input_df.copy()
    for col in columns_to_be_dropped:
        try:
            input_df_m = input_df_m.drop(columns=[col])
        except KeyError:
            pass
    return input_df_m


def color_price(row, price_col_index):
    my_price = row['Price']
    if pd.notnull(my_price):
        my_price = convert_price_to_float(my_price)
        reuter = row['Reuter']
        sanitino = row['Sanitino']
        if reuter == '' and sanitino == '':
            return ['background-color: red' if i == price_col_index else '' for i in range(len(row))]
        elif pd.notnull(reuter) or pd.notnull(sanitino) or reuter != '' or sanitino != '':
            init_list = [my_price, reuter, sanitino]
            list_to_compare = [convert_price_to_float(el) for el in init_list if (el is not None and pd.notnull(el) and el != '')]

            is_target_max = max(list_to_compare) == my_price
            is_target_min = min(list_to_compare) == my_price

            if is_target_min:
                color = 'green'
            elif is_target_max:
                color = 'yellow'
            else:
                color = 'lightblue'

            return [f'background-color: {color}' if i == price_col_index else '' for i in range(len(row))]
        else:
            return ['background-color: red' if i == price_col_index else '' for i in range(len(row))]
    else:
        return [''] * len(row)


def apply_conditional_theme(input_df: pd.DataFrame, output_dir):
    output_dir = os.path.join(output_dir, formatted_current_date())
    create_directory(output_dir)
    output_file_path = os.path.join(output_dir, f"output_{formatted_current_time()}.xlsx")
    price_col_index = input_df.columns.get_loc('Price')
    input_df.style.apply(color_price, args=(price_col_index,), axis=1).to_excel(output_file_path, index=False)

# %% [markdown]
# # Main

# %%
def scrape(input_file: str, output_dir: str, progress_callback=None, progress_msg_callback=None, test=None, scraping_status=None):
    print('Started scraping...')
    if not test:
        # Read the input data
        df = read_input_data(input_file)
        if df is None:
            print('Closing the program...')
            return
        # Remove duplicates
        df = df.drop_duplicates(subset=['Code'])
        # Create 2 extra blank columns
        df['Reuter'] = None
        df['Sanitino'] = None
        # Collect prices
        for index, row in df.iterrows():
            if scraping_status:
                stts = scraping_status()
                if stts is False:
                    break
            code = str(row['Code']).strip()
            formatted_reuter_url = reuter_url.format(code=code)
            dict_data = get_api_data(formatted_reuter_url, site='r')
            msg = f'{index + 1}. received reuter data for {code}'
            if progress_msg_callback:
                progress_msg_callback(msg)
            print(msg)
            try:
                found_data = dict_data.get('data')[0]['model'][0] == code
            except Exception as e:
                print(e)
                found_data = False

            if found_data:
                try:
                    price = dict_data['data'][0]['price']['item']['price']
                    df.at[index, 'Reuter'] = price
                except Exception as e:
                    print(e)
                    print(f"Failed to add data for {code}")
            else:
                pass

            if scraping_status:
                stts = scraping_status()
                if stts is False:
                    break
            formatted_sanitino_url = sanitino_url.format(code=code)
            dict_data2 = get_api_data(formatted_sanitino_url, site='s')
            msg = f'{index + 1}. received sanitino data for {code}'
            if progress_msg_callback:
                progress_msg_callback(msg)
            print(msg)
            try:
                for d in dict_data2['result']['itemListElement']:
                    if 'offers' in d:
                        price2 = d['offers']['price']
                        df.at[index, 'Sanitino'] = price2
            except Exception as e:
                print(e)
            if progress_callback:
                progress = int((index + 1) * 100 / len(df))
                progress_callback(progress)
        # Drop unnecessary columns
        df = drop_unnecessary_columns(df)
        # Replace the nan values with empty string
        df = df.fillna('')
        apply_conditional_theme(df, output_dir)
    else:
        df = read_input_data(input_file)
        if df is None:
            print('Closing the program...')
            return
        for i in range(len(df)):
            if scraping_status:
                stts = scraping_status()
                if stts is False:
                    break
            if progress_callback:
                progress_callback(i)
            if progress_msg_callback:
                progress_msg_callback(f"{i+1}. Completed action {i+1}")
            sleep(1)
                
    return
