# OpenRSC skill experience tracker

Python backend does webscraping from [rsc.vet](https://rsc.vet/) hiscores every two hours with Rocketry for every involved player and parses the received HTML by BeautifulSoup. Then it updates the hiscores variable which Svelte frontend receives through API call.

### [App in Heroku](https://orsc-skilling-competition.herokuapp.com/)

![Frontpage](/client/public/images/client.png)

### Steps to run locally:
1. Docker needs to be installed
2. Run `docker-compose build && docker-compose up` in project root
3. Open `localhost:9000` from your browser (first load takes about 20 seconds per player)

### Running without Docker:
1. From project root `cd client`
2. `npm i`
3. `npm run build`
4. `cd ..`
5. `cd backend`
6. Create python venv
    - Windows:
        - `python -m venv venv` (or python3)
        - `source venv/Scripts/activate`
    - Unix/macOS:
        - `python -m venv venv` (or python3)
        - `source env/bin/activate`
7. `pip install -r requirements.txt`
8. `python -u main.py` (or python3, -u shows scheduler.py logs)
9. Open `localhost:9000` from your browser (first load takes about 20 seconds per player)

### Running the tests
1. For backend tests in folder backend run `pytest`
2. For frontend tests in folder client run `npm run test`

### Configuring for your own needs
1. From backend/players.py file you can change your wanted players with their starting experience of the skill you want.
2. From scheduler.py file search for text "Overall" and replace it with skill of your choice, for example "Agility"
3. From same scheduler.py file you can also change how often the webscraping happens. Though it would be nice not to trigger it too often to not stress test rsc.vet too much.
4. For dummy data testing you can comment the line `return hiscores` from file api.py, and uncomment the line `# return dummy_hiscores`. You should also comment the line `@app.task(every("2 hours"))` from file scheduler.py so it doesn't trigger the scraping for no reason.