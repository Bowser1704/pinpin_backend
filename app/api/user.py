#coding=utf-8

import requests
import simplejson as json
from flask import jsonify, request

from . import api
from .. import db
from ..login import get_id
from ..models import Comment, Orderbuy, Ordercar, User


@api.route('/user/info/',methods=['GET', 'PUT'], endpoint='user_info')
@User.check
def user_info(openid):
    us=User.query.filter_by(openid=openid).first()
    if us is None:
        return jsonify({
            "msg":"no user"
        }),403
    if request.method == 'GET':
        info={
            "username":us.username,
            "headpicture":us.headpicture,
            "openid":us.openid,
            "st_num": us.st_num,
            "wechat" : us.wechat,
            "tel":us.tel,
            "qq":us.qq
        }
        return jsonify({
            "info": info 
        }),200
    elif request.method =='PUT':
        #data=request.get_json()
        if request.is_json:
            us.tel=request.json['tel']
            us.wechat=request.json['wechat']
            us.qq=request.json['qq']
            db.session.add(us)
            db.session.commit()
            return jsonify({
                'msg':'OK'
            }),200
        else:
            return jsonify({
                'msg':'no json'
            }),302

# @api.route("/user/<userID>/",methods=['GET'],endpoint='user_info1')
# @User.check
# def user_info(openid,userID):
#     us=User.query.filter_by(openid=userID).first()
#     if us is None:
#         return jsonify({
#             "msg":"user is not found"
#         })
#     info={
#         "username":us.username,
#         "headpicture":us.headpicture,
#         "openid":us.openid,
#         "st_num": us.st_num,
#         "wechat" : us.wechat,
#         "tel":us.tel,
#         "qq":us.qq
#     }
#     return jsonify({
#         "info": info 
#     }),200
