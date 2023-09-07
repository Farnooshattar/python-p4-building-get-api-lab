#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = []
    for bakery in Bakery.query.all():
       bakery_dict=bakery.to_dict()
       bakeries.append(bakery_dict)

    response = make_response(
        jsonify(bakeries),
        200
        # games,
        # 200,
        # {"Content-Type": "application/json"}
    )

    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery=Bakery.query.filter(Bakery.id==id).first()
    if bakery:
        bakery_dict = bakery.to_dict()
        response = make_response(jsonify(bakery_dict), 200)
    else:
        response = make_response(jsonify({"error": "Bakery not found"}), 404)
    return response


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    bakedgoods = []
    
    for goodies in BakedGood.query.order_by(BakedGood.price.desc()).all():
       goodies_dict = goodies.to_dict()
       bakedgoods.append(goodies_dict)

    response = make_response(
        jsonify(bakedgoods),
        200
        # bakedgoods,
        # 200,
        # {"Content-Type": "application/json"}
    )

    return response
    
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
     
    baked_goods =  BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first() 
  
    baked_dict = baked_goods.to_dict()

    response = make_response(baked_dict, 200)

    

    return response
if __name__ == '__main__':
    app.run(port=5555, debug=True)
