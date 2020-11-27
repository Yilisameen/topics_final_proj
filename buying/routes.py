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
    return 'Hello, World!'

@app.route('/addItemToCart/', methods=['GET','POST'])
def add_item_to_cart():
    uid = int(request.args.get('uid'))
    item_id = int(request.args.get('item_id'))
    if uid and item_id:
        existing_record = Shoppingcart.query.filter(
            and_(Shoppingcart.uid == uid,Shoppingcart.itemid == item_id)
        ).first()
        if existing_record:
            return jsonify(
                status = 'fail',
                reason = 'recording already exist'
            )
        new_record = Shoppingcart(
            uid = uid,
            itemid = item_id,
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
        all_records = db.session.query(Shoppingcart.itemid).filter(Shoppingcart.uid == uid).all()
        for record in all_records:
            print(record)
            records.append(record.itemid)
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

def add_item_to_history(uid, item_id):
    existing_record = Shophistory.query.filter(
        and_(Shophistory.uid == uid,Shophistory.itemid == item_id)
    ).first()
    if existing_record:
        return False
    new_record = Shophistory(
        uid = uid,
        itemid = item_id,
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
        url = 'http://localhost:8080/auction/item/delete/' + str(item)
        result = requests.get(url)
        # result = True
        if result:
            r1 = _delete_item_in_cart(uid, item)
            r2 = add_item_to_history(uid, item)
            if r1 and r2:
                return jsonify(
                    status = 'success'
                )
    return jsonify(
        status = 'fail'
    )
    
def _get_items_in_history(uid):
    records = []
    if uid:
        all_records = db.session.query(Shophistory.itemid).filter(Shophistory.uid == uid).all()
        for record in all_records:
            records.append(record.itemid)
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