from flask import request, render_template, make_response, jsonify
from datetime import datetime as dt
from flask import current_app as app
# from .models import db, User, Watchlist
from .models import db, Shoppingcart, Shophistory
from sqlalchemy import and_
import requests

#for test
@app.route('/')
def hello():
    return jsonify(
        success = True
    )
@app.route('/name')
def hello2():
    return jsonify(
        name = 'name'
    )

@app.route('/addItemToCart/', methods=['GET','POST'])
def add_item_to_cart():
    uid = int(request.args.get('uid'))
    item_id = int(request.args.get('item_id'))
    price = float(request.args.get('price'))
    if uid and item_id:
        existing_record = Shoppingcart.query.filter(
            and_(Shoppingcart.uid == uid,Shoppingcart.itemid == item_id)
        ).first()
        if existing_record:
            return jsonify(
                status = 'fail',
                reason = 'recording already exist'
            )
        # r = requests.get('http://localhost:8080/auction/item/' + str(item_id))
        r = requests.get('http://localhost:23334/name')
        name = r.json()['name']
        new_record = Shoppingcart(
            uid = uid,
            itemid = item_id,
            itemname = name,
            price = price,
            created=dt.now()
        )
        db.session.add(new_record)
        db.session.commit()
    return jsonify(
        status = 'success'
    ), 200

def _get_items_in_cart(uid):
    records = []
    if uid:
        all_records = db.session.query(Shoppingcart.itemid, Shoppingcart.itemname, Shoppingcart.price).filter(Shoppingcart.uid == uid).all()
        for record in all_records:
            item = {
                'item_id': record.itemid,
                'item_name': record.itemname,
                'item_price': record.price
            }
            print(item)
            records.append(item)
    return records

@app.route('/getItemsInCart/', methods=['GET'])
def get_items_in_cart():
    uid = int(request.args.get('uid'))
    records = []
    records = _get_items_in_cart(uid)
    return jsonify(
        uid = uid,
        records = records
    ), 200
    
def _delete_item_in_cart(uid, item_id):
    existing_record = Shoppingcart.query.filter(
        and_(Shoppingcart.uid == uid,Shoppingcart.itemid == item_id)
    ).first()
    if existing_record:
        db.session.delete(existing_record)
        db.session.commit()
        return True
    else:
        return False

@app.route('/deleteItemInCart/', methods=['GET'])
def delete_item_in_cart():
    uid = int(request.args.get('uid'))
    item_id = int(request.args.get('item_id'))
    if uid and item_id:
        r = _delete_item_in_cart(uid, item_id)
        if r:
            return jsonify(
                status = 'success'
            )
        else:
            return jsonify(
                status = 'fail'
            )
    return jsonify(
        status = 'fail'
    )

def add_item_to_history(uid, item_id, item_name, price):
    existing_record = Shophistory.query.filter(
        and_(Shophistory.uid == uid,Shophistory.itemid == item_id)
    ).first()
    if existing_record:
        return False
    new_record = Shophistory(
        uid = uid,
        itemid = item_id,
        itemname = item_name,
        price = price,
        created=dt.now()
    )
    db.session.add(new_record)
    db.session.commit()
    return True

@app.route('/checkout/', methods=['GET', 'POST'])
def checkout():
    uid = uid = int(request.args.get('uid'))
    items = _get_items_in_cart(uid)
    for item in items:
        # r = requests.get('http://localhost:8080/auction/item/delete/' + str(item))
        r = requests.get('http://localhost:23334/')
        if r.json()['success']:
            r1 = _delete_item_in_cart(uid, item['item_id'])
            r2 = add_item_to_history(uid, item['item_id'], item['item_name'], item['item_price'])
            print(r1, r2)
            if not r1 or not r2:
                return jsonify(
                    status = 'fail'
                )
    return jsonify(
        status = 'success'
    )
    
def _get_items_in_history(uid):
    records = []
    if uid:
        all_records = db.session.query(Shophistory.itemid, Shophistory.itemname, Shophistory.price, Shophistory.created).filter(Shophistory.uid == uid).all()
        for record in all_records:
            history = {
                'item_id': record.itemid,
                'item_name': record.itemname,
                'item_price': record.price,
                'item_date': record.created
            }
            records.append(history)
    return records

@app.route('/getShopHistory/', methods=['GET'])
def get_items_in_history():
    uid = int(request.args.get('uid'))
    records = []
    records = _get_items_in_history(uid)
    return jsonify(
        uid = uid,
        records = records
    ), 200