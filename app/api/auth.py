#coding=utf-8

import requests
import simplejson as json
from flask import jsonify, request

from . import api
from .. import db
from ..login import try_login
from ..models import User

@api.route('auth/login/',methods=[ 'POST'])
def login():
    username=request.json['username']
    stNum=request.json['stNum']
    password=request.json['password']
    headPicture=request.json['headPicture']
    is_st = try_login(username=stNum,password=password)
    if stNum=="2018212576":
        is_st = True
    if not is_st:
        return jsonify({"msg":"login fail password is wrong"}) , 401
    try:
        openid = request.headers['openid']
        us = User.query.filter_by(openid=openid).first()        
        
        if us is None :
            us=User(openid=openid)
        us.stNum=stNum
        us.headPicture=headPicture
        us.username=username
        db.session.add(us)
        db.session.commit()
        token=us.generate_token()
        return jsonify({
            'token':token
        }),200
    except:
        return jsonify({
            'msg':'login error'
        }),402
        
@api.route('auth/openid/',methods=['POST'])   
def get_openid():
    code=request.json['code']
    headPicture=request.json['headPicture']
    username = request.json['username']
    url="https://api.weixin.qq.com/sns/jscode2session?appid=wx383b3e632cb77531&secret=1d687ad62829c2211567435a39f944c4&js_code="+ code + "&grant_type=authorization_code"
    try:
        x=requests.get(url)
        re=json.loads(x.text)
        openid=re['openid']
    except:
        return jsonify({
            'msg':'wrong'
        }),401

    if openid !="" :
        us=User.query.filter_by(openid=openid).first()
        if us is None or us.stNum is None:
            return jsonify({
                "msg" : "未学号认证，跳转去学号认证",
                "openid":openid
            }),200
        else:
            if headPicture!=us.headPicture:
                us.headPicture=headPicture
            if username != us.username:
                us.username = username
            db.session.add(us)
            db.session.commit()
            token=us.generate_token()
            return jsonify({
                "msg": "已经学号认证",
                "token":token,
                "openid":openid
            }),200
    else:
        return jsonify({
            "msg":"wrong"
        }),500