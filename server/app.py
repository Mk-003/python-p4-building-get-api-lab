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
    bakeries=[]
    bakeries_query = Bakery.query.all()
    if not bakeries_query:
        return 'No bakeries found', 404
    for bakery in Bakery.query:
        bakery_dict=bakery.to_dict()
        if not bakery_dict:
           return 'Error converting bakery to dict', 500
        bakeries.append(bakery_dict)

    response=make_response(
        bakeries,
        200,
        {"Content-Type": "application/json"}
    )    

    return response

@app.route('/bakeries/<int:id>')
def bakeries_by_id():
    bakery=Bakery.query.filter(Bakery.id==id).first()
    
    if bakery:
    
         backery_dict=bakery.to_dict()
         response=make_response(
            backery_dict,
            200,
            {"Content-Type": "application/json"}
            
        )
    else:
        response = make_response("Bakery not found", 404)

    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods=BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_list = [baked_good.to_dict() for baked_good in baked_goods]

    # Return the list of baked goods as JSON
    return jsonify(baked_goods_list)
    
    






# @app.route('/bakeries/<int:id>')
# def bakery_by_id(id):
#     return ''


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()

    baked_good_dict = most_expensive_baked_good.to_dict()


    return jsonify(baked_good_dict)

if __name__ == '__main__':
    app.run(port=5505, debug=True)
