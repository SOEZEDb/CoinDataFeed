CoinMarketCap Scraper & API
Scrapes cryptocurrency data (name, price, 24h change, market cap) from CoinMarketCap using Playwright and stores it in a SQLite database. Includes a simple Flask API to query the data.
Setup
pip install playwright flask
playwright install chromium
Usage
python main.py   # run the scraper
python api.py    # start the API at localhost:5000
Endpoints
GET /rows — list coins (supports ?name=Bitcoin&page=2)
GET /names — list distinct coin names
