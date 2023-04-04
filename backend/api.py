from flask import Flask
import requests
from bs4 import BeautifulSoup
from players import players

app = Flask(__name__, static_folder='../client/dist', static_url_path='/')

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/api/hiscores')
def get_hiscores():
    hiscores = []
    for player in players:
        new_exp = get_new_exp_from_hiscores(player['playerName'])
        parsed_new_exp = parse_exp(new_exp) 
        hiscores.append(
            { 'playerName': player['playerName'], 'oldExp': player['oldExp'], 'newExp': parsed_new_exp })
    return hiscores

def get_new_exp_from_hiscores(player_name):
    trimmed_player_name = player_name
    if ' ' in trimmed_player_name:
        trimmed_player_name = trimmed_player_name.replace(' ', '%20')

    URL = "https://rsc.vet/player/preservation/" + trimmed_player_name
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'lxml')

    skill_string = soup.find(lambda tag: tag.name == 'a' and 'Agility' in tag.text)
    skill_column = skill_string.find_parent('td')
    skill_row = skill_column.find_parent('tr')

    return skill_row.select_one('td:nth-of-type(6)').text

def parse_exp(new_exp):
    parsed_new_exp = new_exp.replace('\n', '')
    parsed_new_exp = parsed_new_exp.replace(',', '.')
    parsed_new_exp = float(parsed_new_exp)
    return parsed_new_exp

if __name__ == '__main__':
    app.run()  
