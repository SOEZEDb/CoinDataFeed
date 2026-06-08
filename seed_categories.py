from api import app, db
from models import Coin, Category

with app.app_context():
    db.create_all()
    btc = Coin.query.filter_by(name='Bitcoin').first()
    eth = Coin.query.filter_by(name='Ethereum').first()

    if not btc or not eth:
        print("Error: Make sure Bitcoin and Ethereum exist in the database first.")
        exit()

    cat1 = Category(name='DeFi', coin_id=eth.id)
    cat2 = Category(name='Layer1', coin_id=eth.id)
    cat3 = Category(name='Layer1', coin_id=btc.id)

    db.session.add_all([cat1, cat2, cat3])
    db.session.commit()

    for coin in Coin.query.all():
        print(f"{coin.name}: {[c.name for c in coin.categories]}")