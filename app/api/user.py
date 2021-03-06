# coding=utf-8

import requests
import simplejson as json
from flask import jsonify, request

from . import api
from .. import db
from ..login import get_id
from ..models import Comment, Orderbuy, Ordercar, User


@api.route('/user/info/', methods=['GET', 'PUT','POST'], endpoint='user_info')
@User.check
def user_info(openid):
    us = User.query.filter_by(openid=openid).first()
    if us is None:
        return jsonify({
            "msg": "no user"
        }), 403
    if request.method == 'GET':
        info = {
            "username": us.username,
            "headPicture": us.headPicture,
            "openid": us.openid,
            "stNum": us.stNum,
            "wechat": us.wechat,
            "tel": us.tel,
            "qq": us.qq
        }
        return jsonify({
            "info": info
        }), 200
    elif request.method == 'PUT':
        if request.is_json:
            us.tel = request.json['tel']
            us.wechat = request.json['wechat']
            us.qq = request.json['qq']
            db.session.add(us)
            db.session.commit()
            return jsonify({
                'msg': 'OK'
            }), 200
        else:
            return jsonify({
                'msg': 'no json'
            }), 302
    elif request.method == 'POST':
        if request.is_json:
            us.username = request.json['username']
            us.headPicture = request.json['headPicture']
            db.session.add(us)
            db.session.commit()
            return jsonify({
                'msg': 'OK'
            }), 200
        else:
            return jsonify({
                'msg': 'no json'
            }), 302

