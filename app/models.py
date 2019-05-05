# coding=utf-8

import time
import jwt
import datetime
from . import db
from flask import current_app, jsonify, request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from functools import wraps


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(30))
    username = db.Column(db.String(30))
    userPicture = db.Column(db.String(60))
    stNum = db.Column(db.String(30))
    headPicture = db.Column(db.String(30))
    tel = db.Column(db.String(11))
    qq = db.Column(db.String(12))
    wechat = db.Column(db.String(30))

    def __repr__(self):
        return '<User {}>'.format(self.id)

    def generate_token(self, expiration=360000000000):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'openid': self.openid})

    def check(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers['token']
            if token is None:
                return jsonify({
                    "msg": 'no token'
                    }), 401

            s = Serializer(current_app.config['SECRET_KEY'])
            try:
                data = s.loads(token)
            except BaseException:
                return jsonify({
                    'msg': 'token error'
                    }), 401
            openid = data.get('openid')
            if openid is None:
                return jsonify({
                    'msg': 'token error'
                    }), 401
            return f(openid, *args, **kwargs)
        return decorated_function


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime)
    time = db.Column(db.String(60))
    # 订单启动时间，可能是购买，可能是出发
    tel = db.Column(db.String(11), nullable=True)
    qq = db.Column(db.String(12), nullable=True)
    wechat = db.Column(db.String(30), nullable=True)
    numNeed = db.Column(db.Integer)
    numExist = db.Column(db.Integer)
    heading = db.Column(db.String(20))
    content = db.Column(db.String(120))
    postID = db.Column(db.String(30))
    full = db.Column(db.Integer)
    # -------


class Orderbuy(Order):
    kind = db.Column(db.Integer)
    location = db.Column(db.String(60))
    picture = db.Column(db.String(120))


class Ordercar(Order):
    placeA = db.Column(db.String(50), index=True)
    placeB = db.Column(db.String(50), index=True)


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime)
    content = db.Column(db.Text)
    #kind = db.Column(db.Integer,index=True)
    # 1为购物，2为拼车
    orderbuyID = db.Column(db.Integer, index=True, default=-1)
    ordercarID = db.Column(db.Integer, index=True, default=-1)
    userID = db.Column(db.String(30), index=True)


# 有一个db.Table类可以直接定义多对多表
class Pick2order(db.Model):
    __tablename__ = 'u2orders'
    kind = db.Column(db.Integer, index=True)
    #定义是car or buy
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.String(60), index=True)
    orderID = db.Column(db.Integer, index=True)

# 发起


class Post2order(db.Model):
    __tablename__ = 'p2orders'
    kind = db.Column(db.Integer, index=True)
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.String(60), index=True)
    orderID = db.Column(db.Integer, index=True)
