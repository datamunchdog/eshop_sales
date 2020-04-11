# -*- coding: utf-8 -*-
"""

Metacritic data for Switch games

"""

# Import modules
from bs4 import BeautifulSoup as bs
import requests

# Set User-Agent:
user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}

# Define functions:
def get(url):
    """GET request"""
    r = requests.get(url, headers=user_agent)
    text = r.text
    return text
    
# Get App ID, API Key:
url = 'https://www.metacritic.com/browse/games/release-date/available/switch/metascore?page={}'

all_games = []
for x in range(2):
    html = get(url.format(x))
    soup = bs(html, 'html.parser')
    first_game = soup.find('li', {'class': 'product game_product first_product'})
    games = soup.find_all('li', {'class': 'product game_product'})
    last_game = soup.find('li', {'class': 'product game_product last_product'})
    games.extend([first_game, last_game])
    all_games.extend(games)

game_data = []
for game in all_games:


    title = game.find('div', {'class': 'basic_stat product_title'})

    if game.find('div', {'class': 'metascore_w small game positive'}):
        metascore = game.find('div', {'class': 'metascore_w small game positive'})
    else:
        metascore = game.find('div', {'class': 'metascore_w small game mixed'})
    if game.find('span', {'class': 'data textscore textscore_favorable'}):
        user_score = game.find('span', {'class': 'data textscore textscore_favorable'})
    else:
        user_score = game.find('span', {'class': 'data textscore textscore_mixed'})


    raw_data = {'title': title,'metascore': metascore,'user_score': user_score}
    
    clean_data = {}
    for k, v in raw_data.items():
        try:
            clean_data[k] = v.text.strip()
        except:
            clean_data[k] = '' 
    game_data.append(clean_data)
    
