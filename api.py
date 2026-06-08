from flask import Flask, jsonify, request
from models import db,Coin,Category
import os


basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'coinmarketcap.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def coin_to_dict(coin):
    return {
        'id': coin.id,
        'name': coin.name,
        'price': coin.price,
        'change_24h': coin.change_24h,
        'market_cap': coin.market_cap,
    }

@app.route("/rows")
def  get_rows():
    name = request.args.get('name')
    page = request.args.get('page', 1, type=int)
    per_page = 20
    query = Coin.query
    if name:
        query = query.filter_by(name=name)

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    coins = pagination.items

    return jsonify([coin_to_dict(coin) for coin in coins])

@app.route("/names")
def get_names():
    names = db.session.query(Coin.name).distinct().limit(20).all()
    return jsonify([row[0] for row in names])


@app.route("/coins/category/<category_name>")
def get_coins_by_category(category_name):
    coins = Coin.query.join(Category).filter(Category.name == category_name).all()
    return jsonify([coin_to_dict(coin) for coin in coins])

@app.route("/coins/top10")
def get_top10():
    coins = Coin.query.order_by(Coin.price.desc()).limit(10).all()
    return jsonify([coin_to_dict(coin) for coin in coins])

@app.route("/coins/search")
def search_coins():
    search = request.args.get('search')
    coins = Coin.query.filter(Coin.name.contains(search)).all()
    return jsonify([coin_to_dict(coin) for coin in coins])

@app.route("/coins/active")
def get_active_coins():
    coins = Coin.query.filter(Coin.change_24h != "N/A").all()
    return jsonify([coin_to_dict(coin) for coin in coins])

@app.route("/coins/alphabetical")
def get_alphabetical_coins():
    coins = Coin.query.order_by(Coin.price.asc()).limit(10).all()
    return jsonify([coin_to_dict(coin) for coin in coins])

if __name__ == "__main__":
    app.run(debug=True)

