# OpenRSC experience tracker

README and project still under construction

Python backend does webscraping from [rsc.vet](https://rsc.vet/) hiscores once a day at midnight UTC time with Rocketry for every involved player and parses the received HTML by BeautifulSoup. Hiscores and Players are saved to PostgreSQL database. Svelte frontend receives the data through API call.

### [App in Heroku](https://openrsc-exp-tracker.herokuapp.com/)

![Frontpage](/client/public/images/client.png)

### Steps to run locally:
1. Docker needs to be installed
2. Run `./start.sh` in project root
3. Open `localhost:9000` from your browser (first load takes about 20 seconds per player)

### Running without Docker:
1. From project root `cd client`
2. `npm i`
3. `npm run autobuild` (this will build client automatically when modifying files)
4. Open new terminal
5. `cd backend`
6. Create python venv
    - Windows:
        - `python -m venv venv` (or python3, this needs to be run only first time)
        - `source venv/Scripts/activate`
    - Unix/macOS:
        - `python -m venv venv` (or python3)
        - `source env/bin/activate`
7. `pip install -r requirements.txt`
8. `python -u main.py` (or python3, -u shows scheduler.py logs)
9. Open `localhost:9000` from your browser (first load takes about 20 seconds per player)

### Running the tests

Tests currently work in progress
1. For backend tests in folder backend run `pytest`
2. For frontend tests in folder client run `npm run test`

### Configuring for your own needs
1. You can add Players through API with for example Postman
    - POST request to http://localhost:9000/api/players with JSON body:
    ```
    {
      "name": "Test Name",
      "original_exp": 1002003
    }
    ```
2. From scheduler.py file search for text "Overall" and replace it with skill of your choice, for example "Agility"
3. From same scheduler.py file you can also change how often the webscraping happens. Though it would be nice not to trigger it too often to not stress test rsc.vet too much.
4. Dummy test data generating script work in progress
5. You might want to comment out the task from file scheduler.py so it doesn't trigger the scraping if you don't need it. If you for example create the data manually through API call or straight to the database.

### Technology keywords
- Python backend
- Svelte frontend
- FastAPI web framework
- Rocketry task scheduler
- Beautiful Soup for parsing HTML
- PostgreSQL database
- Heroku deployment environment