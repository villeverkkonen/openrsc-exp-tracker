# OpenRSC skill experience tracker

Python backend does webscraping from rsc.vet hiscores every hour for every involved player and parses the received HTML by BeautifulSoup. Then it updates the hiscores variable which Svelte frontend receives through API call.

In frontend we can show each players starting and so far gained experience and possibly do some visual graphics with that data.