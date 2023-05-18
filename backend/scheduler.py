import time
import os
import httpx
from bs4 import BeautifulSoup
from rocketry import Rocketry
from rocketry.conds import cron

app = Rocketry(config={"task_execution": "async"})


API_BASE_URL = os.getenv("API_URL", "http://localhost:9000")


# Run once a day at midnight
@app.task(cron("0 0 * * *"))
# @app.task('every 30 minutes')
# @app.task('every 1 hour')
async def update_hiscores():
    print('Starting hiscores update')

    players = []
    async with httpx.AsyncClient() as client:
        GET_PLAYERS_URL = API_BASE_URL + "/api/players"
        players_response = await client.get(GET_PLAYERS_URL, timeout=10.0)
        players = players_response.json()

        for index, player in enumerate(players):
            print('Updating hiscores for player: ' + player['name'])
            new_exp = await get_new_exp_from_hiscores(player['name'], client)
            parsed_new_exp = parse_exp(new_exp)
            total_gained_exp = parsed_new_exp - player['original_exp']

            hiscore = {"new_exp": parsed_new_exp,
                       "total_gained_exp": total_gained_exp}
            CREATE_HISCORE_URL = API_BASE_URL + \
                "/api/players/" + str(player['id']) + "/hiscores"
            hiscore_response = await client.post(CREATE_HISCORE_URL, json=hiscore, timeout=10.0)
            print("Created hiscore:")
            print(hiscore_response.json())

            if index < len(players) - 1:
                # We don't want to burden rsc.vet too much too fast
                time.sleep(15)
        print('Hiscores updated!')


async def get_new_exp_from_hiscores(player_name, client):
    trimmed_player_name = player_name
    if ' ' in trimmed_player_name:
        trimmed_player_name = trimmed_player_name.replace(' ', '%20')

    URL = "https://rsc.vet/player/preservation/" + trimmed_player_name
    response = await client.get(URL, timeout=10.0)
    soup = BeautifulSoup(response.content, 'lxml')

    skill_string = soup.find(lambda tag: tag.name ==
                             'a' and 'Overall' in tag.text)
    skill_column = skill_string.find_parent('td')
    skill_row = skill_column.find_parent('tr')

    return skill_row.select_one('td:nth-of-type(6)').text


def parse_exp(new_exp):
    # Exp comes in a form of \n2,337,597\n
    # Trim it so it can be parsed to int
    parsed_new_exp = new_exp.replace('\n', '')
    parsed_new_exp = new_exp.replace(',', '')
    parsed_new_exp = int(parsed_new_exp)
    return parsed_new_exp


if __name__ == "__main__":
    app.run()
