from flask import request, render_template, make_response, jsonify
from datetime import datetime as dt
from flask import current_app as app
from .models import db, User, Watchlist
from sqlalchemy import and_
import requests

#for test
@app.route('/')
def hello():
    return jsonify(
        id = '5',
        name = 'name'
    )

def is_user_admin_or_suspend(uid, op):
    result = False
    if op == 'isAdmin':
        r = db.session.query(User.admin).filter(User.uid == uid).first()
        if r.admin:
            result = True
    elif op == 'isSuspend':
        r = db.session.query(User.suspend).filter(User.uid == uid).first()
        if r.suspend:
            result = True
    return result

@app.route('/isAdmin/', methods=['GET'])
def is_user_admin():
    result = False
    uid = int(request.args.get('uid'))
    if uid:
        result = is_user_admin_or_suspend(uid, 'isAdmin')
    return jsonify(
        is_admin = result
    ), 200

@app.route('/isSuspend/', methods=['GET'])
def is_user_suspend():
    result = False
    uid = int(request.args.get('uid'))
    if uid:
        result = is_user_admin_or_suspend(uid, 'isSuspend')
    return jsonify(
        is_suspend = result
    ), 200

@app.route('/userCreate/', methods=['POST', 'GET'])
def user_create():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    bio = request.form['user_bio']
    # username = 'test4'
    # email = 'test4@test.com'
    # password = 'test4'
    # bio = 'test user4'
    if username and email:
        existing_user = User.query.filter(
            User.username == username or User.email == email
        ).first()
        if existing_user:
            # return make_response(
            #     f'{username} ({email}) already created!'
            # )
            return jsonify(
                status = 'fail',
                reason = 'user already existed'
            ), 200
        new_user = User(
            username=username,
            email=email,
            password=password,
            credibility=5.0,
            created=dt.now(),
            bio=bio,
            admin=False,
            suspend=False,
        )
        db.session.add(new_user)  # Adds new User record to database
        db.session.commit()
    return jsonify(
        status = 'success'
    ), 201

@app.route('/userDelete/', methods=['POST', 'GET'])
def user_delete():
    uid = int(request.args.get('uid'))
    if uid:
        existing_user = db.session.query(User).get(uid)
        if existing_user:
            db.session.delete(existing_user)
            db.session.commit()
            # return make_response('Delete successfully!')
            #return True
            return jsonify(
                status = 'success'
            ), 200
        else:
            return jsonify(
                status = 'fail',
                reason = 'user not existed'
            ), 200
    return jsonify(
        status = 'fail',
        reason = 'uid missed'
    ), 200

@app.route('/userSuspend/', methods=['POST', 'GET'])
def user_suspend():
    uid = int(request.args.get('uid'))
    if uid:
        existing_user = db.session.query(User).get(uid)
        if existing_user:
            existing_user.suspend = True
            db.session.commit()
            # return make_response('Suspend successfully')
            #return True
            return jsonify(
                status = 'success'
            ), 200
        else:
            # return make_response('User not existed')
            #return False
            return jsonify(
                status = 'fail',
                reason = 'user not existed'
            ), 200
    return jsonify(
        status = 'fail',
        reason = 'uid missed'
    ), 200

@app.route('/getUserInfo/', methods=['GET'])
def get_user_info():
    uid = int(request.args.get('uid'))
    if uid:
        user_info = db.session.query(User).get(uid)
        if user_info:
            return jsonify(
                status = 'success',
                username = user_info.username,
                email = user_info.email
            ), 200
    return jsonify(
        status = 'fail',
        reason = 'uid not right or missed'
    ), 200

@app.route('/login/', methods=['GET'])
def user_login():
    email = request.form['email']
    password = request.form['password']
    # email = 'test4@test.com'
    # password = 'test'
    if email and password:
        user_info = db.session.query(User.password, User.uid, User.admin).filter(User.email == email).first()
        if user_info and user_info.password == password:
            return jsonify(
                status = 'success',
                user_id = user_info.uid,
                admin = user_info.admin
            ), 200
        else:
            return jsonify(
                status = 'fail',
                reason = 'email or password is not right'
            ), 200
    return jsonify(
            status = 'fail',
            reason = 'email or password missed'
        ), 200

@app.route('/fetchUserIdentity/', methods=['GET'])
def fetch_user_identity():
    uid = int(request.args.get('uid'))
    if uid:
        user_info = db.session.query(User.username, User.email, User.suspend).filter(User.uid == uid).first()
        if user_info:
            return jsonify(
                status = 'success',
                username = user_info.username,
                email = user_info.email,
                suspend = user_info.suspend
            ), 200
        else:
            return jsonify(
                status = 'fail',
                info = 'user not exits'
            ), 200
    return jsonify(
        status = 'fail',
        info = 'uid missed'
    ), 200

@app.route('/addItemToWatchlist/', methods=['GET', 'POST'])
def add_item_to_watchlist():
    uid = int(request.args.get('uid'))
    item_id = int(request.args.get('item_id'))
    criteria = float(request.args.get('criteria'))
    if uid and item_id:
        existing_record = Watchlist.query.filter(
            and_(Watchlist.uid == uid,Watchlist.itemid == item_id)
        ).first()
        if existing_record:
            return jsonify(
                status = 'fail',
                reason = 'recording already exist'
            )
        # r = requests.get('http://localhost:8080/auction/item/' + str(item_id))
        r = requests.get('http://localhost:23333/')
        name = r.json()['name']
        new_record = Watchlist(
            uid = uid,
            itemid = item_id,
            itemname = name,
            created = dt.now(),
            criteria = criteria
        )
        db.session.add(new_record)
        db.session.commit()
    return jsonify(
        status = 'success'
    )

@app.route('/getItemsInWatchlist/', methods=['GET'])
def get_items_in_watchlist():
    uid = int(request.args.get('uid'))
    records = []
    if uid:
        all_records = db.session.query(Watchlist.itemid, Watchlist.itemname, Watchlist.criteria).filter(Watchlist.uid == uid).all()
        for record in all_records:
            print(record)
            item = {
                'item_name': record.itemname,
                'item_id': record.itemid,
                'criteria': record.criteria
            }
            records.append(item)
        return jsonify(
            uid = uid,
            records = records
        )

@app.route('/meetCriteria/')
def users_meet_criteria():
    item_id = int(request.args.get('item_id'))
    price = float(request.args.get('price'))
    if item_id and price:
        infos = []
        all_users = db.session.query(Watchlist.uid, Watchlist.criteria).filter(and_(Watchlist.itemid == item_id, Watchlist.criteria >= price)).all()
        for user in all_users:
            print(user)
            user_info = db.session.query(User).get(user.uid)
            print(user_info)
            if user_info:
                info = {
                    'uid': user_info.uid,
                    'username': user_info.username,
                    'email': user_info.email,
                    'criteria': user.criteria
                }
                infos.append(info)
        return jsonify(
            all_users = infos,
            status = 'success'
        )
    return jsonify(
        status = 'fail'
    )

    