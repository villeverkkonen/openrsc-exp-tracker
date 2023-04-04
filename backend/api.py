from flask import Flask
import requests
from bs4 import BeautifulSoup

app = Flask(__name__, static_folder='../client/dist', static_url_path='/')

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/api/hiscores')
def get_hiscores():
    URL = "https://rsc.vet/player/preservation/Lord%20Jolt"
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    row = soup.select_one('table tbody tr:nth-of-type(16)')
    expColumn = row.select_one('td:nth-of-type(6)').text
    
    return expColumn

if __name__ == '__main__':
    app.run()  
