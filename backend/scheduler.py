import time
import requests
from bs4 import BeautifulSoup
from rocketry import Rocketry
from rocketry.conds import every
from hiscores import hiscores
from players import players

app = Rocketry(config={"task_execution": "async"})

@app.task(every("5 seconds"))
async def test():
    print('TEST')

# @app.task(every("2 minutes"))
async def update_hiscores():
    print('Starting hiscore update')
    hiscores.clear()
    for index, player in enumerate(players):
        print('Fetching hiscores for player: ' + player['playerName'])
        new_exp = get_new_exp_from_hiscores(player['playerName'])
        parsed_new_exp = parse_exp(new_exp)
        hiscores.append(
            {
                'playerName': player['playerName'],
                'oldExp': player['oldExp'],
                'newExp': parsed_new_exp,
                'gainedExp': parsed_new_exp - player['oldExp']
            }
        )
        if index < len(players) - 1:
            # We don't want to burden rsc.vet too much too fast
            time.sleep(15)

    hiscores.sort(key=lambda x: x['gainedExp'], reverse=True)
    print('Hiscores updated!')


def get_new_exp_from_hiscores(player_name):
    trimmed_player_name = player_name
    if ' ' in trimmed_player_name:
        trimmed_player_name = trimmed_player_name.replace(' ', '%20')

    URL = "https://rsc.vet/player/preservation/" + trimmed_player_name
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'lxml')

    skill_string = soup.find(lambda tag: tag.name ==
                             'a' and 'Overall' in tag.text)
    skill_column = skill_string.find_parent('td')
    skill_row = skill_column.find_parent('tr')

    return skill_row.select_one('td:nth-of-type(6)').text


def parse_exp(new_exp):
    # Exp comes in a form of \n2,337,597\n
    # Trim it so it can be parsed to float
    parsed_new_exp = new_exp.replace('\n', '')
    strToReplace = ','
    replacementStr = '.'
    # Change last ',' to '.'
    pos = parsed_new_exp.rfind(strToReplace)
    if pos > -1:
        parsed_new_exp = parsed_new_exp[:pos] + replacementStr + \
            parsed_new_exp[pos + len(strToReplace):]
    # Remove other commas
    parsed_new_exp = parsed_new_exp.replace(',', '')
    parsed_new_exp = float(parsed_new_exp)
    return parsed_new_exp


if __name__ == "__main__":
    app.run()
