from flask import request, render_template, make_response, jsonify
from datetime import datetime as dt
from flask import current_app as app
from .models import db, User

#for test
@app.route('/')
def hello():
    return 'Hello, World!'

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
        is_admin = result
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
            credibility=0.5,
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
    # password = 'test4'
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