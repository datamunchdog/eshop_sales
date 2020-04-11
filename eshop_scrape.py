# -*- coding: utf-8 -*-
"""

Eshop sales

"""

# Import modules
import csv
import json
import math
import requests
import time

import metacritic_switch as ms

# Set User-Agent:
user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}

# Define functions:
def get(url):
    """GET request"""
    r = requests.get(url, headers=user_agent)
    text = r.text
    return text

def post(url, payload):
    """POST request"""
    r = requests.post(url, headers=user_agent, data=payload)
    text = r.text
    return text
    
# Get App ID, API Key:
base_url = 'https://www.nintendo.com/games/game-guide/'

html = get(base_url)
app_id = html[html.find('appId:')+8: html.find('appId:')+18]
api_key = html[html.find('searchApiKey:')+15: html.find('searchApiKey:')+47]

# API URL:
api_url = 'https://u3b6gr4ua3-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.33.0)%3B%20Browser%20(lite)%3B%20JS%20Helper%202.20.1&x-algolia-application-id={}&x-algolia-api-key={}'

# POST request payload/form data:
payload = '{"requests":[{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=42&maxValuesPerFacet=30&page={}&facets=%5B%22generalFilters%22%2C%22platform%22%2C%22availability%22%2C%22categories%22%2C%22filterShops%22%2C%22virtualConsole%22%2C%22characters%22%2C%22priceRange%22%2C%22esrb%22%2C%22filterPlayers%22%5D&tagFilters=&facetFilters=%5B%5B%22generalFilters%3ADeals%22%5D%5D"},{"indexName":"noa_aem_game_en_us","params":"query=&hitsPerPage=1&maxValuesPerFacet=30&page={}&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&facets=generalFilters"}]}'

sale_list = []
# Get first page and number of pages to loop through:
first_payload = payload.replace('{}', '0')
data = json.loads(post(api_url.format(app_id, api_key), first_payload))
number_deals = data['results'][1]['facets']['generalFilters']['Deals']
number_pages = math.ceil((number_deals / 42))

print('Qty deals complete.')
time.sleep(2)

sale_list = []
# Loop through to get all sales, add to 'Sales' list:
for each in range(number_pages):
    next_payload = payload.replace('{}', str(each))
    data = json.loads(post(api_url.format(app_id, api_key), next_payload))
    next_page = data['results'][0]['hits']
    sale_list.extend(next_page)
    print(each, 'done.')
    time.sleep(2)

# Clean sale_list:
clean_sale_list = []
for sale in sale_list:
    data = {'title': sale['title'],
            'nsuid': sale['nsuid'],
            'platform': sale['platform'],
            'msrp': sale['msrp'],
            'sale': sale['salePrice'],
            }
    clean_sale_list.append(data)
    
# Metacritic data:  
metacritic_data = ms.game_data
meta_list = [each['title'] for each in metacritic_data]

# Add only game sales in top 200/400/600/etc. to 'good_sales' list:
good_sales = []
for each in clean_sale_list:
    if each['title'] in meta_list and each['platform'] == 'Nintendo Switch':
        good_sales.append(each)

# Merge Metacritic scoring data into Eshop Sale data:
for sale in good_sales:
    for each in metacritic_data:
        if sale['title'] == each['title']:
            sale['metascore'] = each['metascore']
            sale['user_score'] = each['user_score']

# Sort by Metacritic score:
good_sales = sorted(good_sales, key=lambda k: k['metascore'], reverse=True)
  
# Output to CSV file:    
keys = good_sales[0].keys()
with open('eshop_sales.csv', 'w', newline='') as f:
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(good_sales)










