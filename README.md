CoinMarketCap Scraper & API
Scrapes cryptocurrency data (name, price, 24h change, market cap) from CoinMarketCap using Playwright and stores it in a SQLAlchemy database. Includes a simple Flask API to query the data.
Setup
pip install playwright flask
playwright install chromium
Usage
python main.py   # run the scraper
python api.py    # start the API at localhost:5000

Endpoints
GET /rows — list coins (supports ?name=Bitcoin&page=2)
GET /names — list distinct coin names
GET /names	Returns a list of distinct coin names
GET /rows	Returns paginated coin data. Supports ?name=Bitcoin and ?page=2
GET /coins/search	Search coins by name. Usage: ?search=eth
GET /coins/top10	Returns the top 10 coins by price
GET /coins/category/:name	Returns all coins belonging to a specific category
GET /coins/active	Returns coins with a valid 24h change value
GET /coins/alphabetical	Returns coins sorted alphabetically by name

LIVE API
https://coindatafeed-production.up.railway.app/rows
