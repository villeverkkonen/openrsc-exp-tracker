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
        playerName = player['playerName']
        if ' ' in playerName:
            playerName = playerName.replace(' ', '%20')

        URL = "https://rsc.vet/player/preservation/" + playerName
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html5lib')
        row = soup.select_one('table tbody tr:nth-of-type(16)')
        newExp = parseExpFromRow(row)
        
        hiscores.append(
            { 'playerName': player['playerName'], 'oldExp': player['oldExp'], 'newExp': newExp })

    return hiscores

def parseExpFromRow(row):
    newExp = row.select_one('td:nth-of-type(6)').text
    newExp = newExp.replace('\n', '')
    newExp = newExp.replace(',', '.')
    newExp = float(newExp)
    return newExp

if __name__ == '__main__':
    app.run()  
