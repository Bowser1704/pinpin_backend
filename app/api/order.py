# coding=utf-8

import requests
import os
import simplejson as json
from flask import jsonify, request
import datetime
import qiniu.config

from qiniu import Auth, put_file, etag, urlsafe_base64_encode
from . import api
from .. import db
from ..login import get_id
from ..models import Comment, Orderbuy, Ordercar, User, Post2order, Pick2order

# 添加订单,获取订单，加入订单。
@api.route('/order/post/buy/', methods=['POST','PUT'], endpoint="add_order_buy")
@User.check
def order(openid):
    if request.method == 'POST':
        # 添加订单
        data = request.get_json()
        order = Orderbuy(postID=openid, datetime=datetime.datetime.utcnow())
        order.kind = data.get('kind')
        order.location = data.get('location')
        order.time = data.get('timeBuy')
        order.numNeed = data.get('numNeed')
        order.heading = data.get('heading')
        order.content = data.get('content')
        order.tel = data.get('tel')
        order.qq = data.get('qq')
        order.wecaht = data.get('wechat')
        order.picture = data.get('picture')
        # ；隔开每一个picture_url
        # 内容非必填
        # 联系方式加入订单三个字段
        order.numExist = 1
        db.session.add(order)
        db.session.commit()
        orderID = order.id
        P2order = Post2order(kind=1, userID=openid, orderID=orderID)
        db.session.add(P2order)
        db.session.commit()
        return jsonify({
            'orderID': orderID
        }), 200
    elif request.method == 'PUT':
        # 更新订单
        data = request.get_json()
        order = Orderbuy.query.filter_by(id=orderID).first()
        order.kind = data.get('kind')
        order.location = data.get('location')
        order.time = data.get('timeBuy')
        order.numNeed = data.get('numNeed')
        order.heading = data.get('heading')
        order.content = data.get('content')
        order.tel = data.get('tel')
        order.qq = data.get('qq')
        order.wecaht = data.get('wechat')
        order.picture = data.get('picture')
        # ；隔开每一个picture_url
        # 内容非必填
        # 联系方式加入订单三个字段
        db.session.add(order)
        db.session.commit()
        return jsonify({
            'msg': "ok"
        }), 200


@api.route('/order/buy/', methods=['POST', 'GET'], endpoint="order_buy")
@User.check
def order(openid):
    orderID = request.args.get("orderID", -1, type=int)
    if orderID == -1:
        return jsonify({
            "msg": "no orderID"
        }), 401
    if request.method == 'POST':
        # 加入订单
        order = Orderbuy.query.filter_by(id=orderID).first()
        userID = request.json['userID']
        # 保险机制，确保加入订单
        if str(userID) == openid:
            if order.numExist >= order.numNeed:
                return jsonify({
                    "msg": "order is full"
                }), 403

            if order.postID == str(openid):
                return jsonify({
                    "msg": "you are the poster"
                }), 403
            pick_user = Pick2order.query.filter_by(kind=1, userID=openid, orderID=orderID).first()
            if pick_user:
                way = {
                    'tel': order.tel,
                    "wechat": order.wechat,
                    "qq": order.qq
                }
                return jsonify({
                    'way': way
                }), 200
            if order.postID != str(openid):
                order.numExist += 1
                if order.numExist == order.numNeed:
                    order.full = 1
                p = Pick2order(kind=1, userID=openid, orderID=orderID)
                db.session.add(p, order)
                db.session.commit()
                way = {
                    'tel': order.tel,
                    "wechat": order.wechat,
                    "qq": order.qq
                }
                return jsonify({
                    'way': way
                }), 200
        return jsonify({
            "msg": "不是原用户"
        }), 401

    if request.method == "GET":
        order = Orderbuy.query.filter_by(id=orderID).first()
        if order:
            info = {
                'datetime': order.datetime,
                'kind': order.kind,
                'location': order.location,
                'timeBuy': order.time,
                'picture': order.picture,
                'heading': order.heading,
                'content': order.content,
                'numNeed': order.numNeed,
                'numExist': order.numExist
            }
            # userPicture = []
            postUser = User.query.filter_by(openid=str(order.postID)).first()
            # userPicture.append(postUser.headPicture)
            # P2order = Pick2order.query.filter_by(kind=1, orderID=orderID).all()
            # if P2order:
            #     for u in P2order:
            #         us = User.query.filter_by(openid=u.userID).first()
            #         userPicture.append(us.headPicture)
            info['user_picture'] = postUser.headPicture
            info['username'] = postUser.username
            
            commentss = Comment.query.filter_by(orderbuyID=orderID).all()
            comments = []
            for c in commentss:
                us = User.query.filter_by(openid=str(c.userID)).first()
                x = {
                    'datetime': c.datetime,
                    'content': c.content,
                    'headPicture': us.headPicture,
                    'username': us.username
                }
                comments.append(x)

            data = {
                "info": info,
                "comments": comments
                }
            return jsonify({
                'data': data
            }), 200
        return jsonify({
            "msg" : 'order is not exist'
        }),404


# 添加订单.
@api.route('/order/post/car/', methods=['POST','PUT'], endpoint="add_order_car")
@User.check
def order(openid):
    if request.method == 'POST':
        data = request.get_json()
        order = Ordercar(postID=openid, datetime=datetime.datetime.utcnow())
        order.placeB = data.get('placeB')
        order.placeA = data.get('placeA')
        order.time = data.get('timeGo')
        order.numNeed = data.get('numNeed')
        order.heading = data.get('heading')
        order.content = data.get('content')
        order.tel = data.get('tel')
        order.qq = data.get('qq')
        order.wecaht = data.get('wechat')
        # ；隔开每一个picture_url
        # 内容非必填
        # 联系方式加入订单三个字段
        order.numExist = 1
        db.session.add(order)
        db.session.commit()
        orderID = order.id
        P2order = Post2order(kind=2, userID=openid, orderID=orderID)
        db.session.add(P2order)
        db.session.commit()
        return jsonify({
            'orderID': orderID
        }), 200
    elif request.method == 'PUT':
        data = request.get_json()
        orderID = data.get('orderID')
        order = Ordercar.query.filter_by(id=orderID).first()
        order.placeB = data.get('placeB')
        order.placeA = data.get('placeA')
        order.time = data.get('timeGo')
        order.numNeed = data.get('numNeed')
        order.heading = data.get('heading')
        order.content = data.get('content')
        order.tel = data.get('tel')
        order.qq = data.get('qq')
        order.wecaht = data.get('wechat')
        db.session.add(order)
        db.session.commit()
        return jsonify({
            "msg" : "OK"
        }),200


@api.route("/order/car/", methods=['POST', 'GET'], endpoint="order_car")
@User.check
def order(openid):
    orderID = request.args.get("orderID", -1, type=int)
    if orderID == -1:
        return jsonify({
            "msg": "no orderID"
        }), 401
    if request.method == 'POST':
        # 加入订单
        order = Ordercar.query.filter_by(id=orderID).first()
        userID = request.json['userID']
        # 保险机制，确保加入订单
        if userID == openid:
            if order.numExist >= order.numNeed:
                return jsonify({
                    "msg": "order is full"
                }), 403

            if order.postID == str(openid):
                return jsonify({
                    "msg": "you are the poster"
                }), 403

            pick_user = Pick2order.query.filter_by(kind=2,userID=openid,orderID=orderID).first()
            if pick_user:
                way = {
                    'tel': order.tel,
                    "wechat": order.wechat,
                    "qq": order.qq
                }
                return jsonify({
                    'way': way
                }), 200

            if order.postID != str(openid):
                order.numExist += 1
                if order.numExist == order.numNeed:
                    order.full = 1
                p = Pick2order(kind=2, userID=openid, orderID=orderID)
                db.session.add(p, order)
                db.session.commit()
                way = {
                    'tel': order.tel,
                    "wechat": order.wechat,
                    "qq": order.qq
                }
                return jsonify({
                    'way': way
                }), 200


@api.route('/order/buy/list/', methods=['GET'])
def order_list():
    kind = request.args.get('kind', 1, type=int)
    page = request.args.get('page', 1, type=int)
    pagination = Orderbuy.query.filter_by(kind=kind).order_by(Orderbuy.full, Orderbuy.datetime.desc()).paginate(page, per_page=10, error_out=False)
    orderlist = []
    
    for item in pagination.items:
        userPicture = []
        postUser = User.query.filter_by(openid=str(item.postID)).first()
        if postUser:
            userPicture.append(postUser.headPicture)    
            P2order = Pick2order.query.filter_by(kind=1, orderID=item.id).all()
            if P2order:
                for u in P2order:
                    us = User.query.filter_by(openid=u.userID).first()
                    userPicture.append(us.headPicture)
            while None in userPicture:
                userPicture.remove(None)
            
            order = {
                'datetime' : item.datetime,
                'orderbuyID': item.id,
                'heading': item.heading,
                'timeBuy': item.time,
                'location': item.location,
                'numExist': item.numExist,
                'numNeed': item.numNeed,
                'content': item.content,
                "picture": item.picture,
                "userPicture": userPicture
            }
            orderlist.append(order)
    data = {
        'pageNum': pagination.page,
        'pageMax': pagination.pages,
        'hasNext': pagination.has_next,
        'ordersnum': pagination.total,
        'orderList': orderlist
    }

    return jsonify({
        'data': data
    }), 200


@api.route('/order/car/list/', methods=['GET'], endpoint='order_list1')
def order_list():
    page = request.args.get('page', 1, type=int)
    pagination = Ordercar.query.order_by(Ordercar.full, Ordercar.datetime.desc()).paginate(page, per_page=10, error_out=False)
    orderlist = []
    for item in pagination.items:
        order = {
            'datetime' : item.datetime,
            'ordercarID': item.id,
            'heading': item.heading,
            'timeGo': item.time,
            'placeA': item.placeA,
            'placeB': item.placeB,
            'numExist': item.numExist,
            'numNeed': item.numNeed
        }
        orderlist.append(order)
    data = {
        'pageNum': pagination.page,
        'pageMax': pagination.pages,
        'hasNext': pagination.has_next,
        'ordersnum': pagination.total,
        'orderList': orderlist
    }

    return jsonify({
        'data': data
    }), 200

# 添加评论
@api.route('/order/comments/buy/', methods=['POST'], endpoint="commentBuy")
@User.check
def comment(openid):
    orderID = request.args.get("orderID", -1, type=int)
    if orderID == -1:
        return jsonify({
            "msg": "加上orderID参数"
        }), 402
    #print("I am here!!!!!!!!!!!!!!!")
    userID = request.json.get('userID')
    content = request.json.get('content')
    print(userID)
    print(openid)
    if str(userID) == str(openid):
        comment = Comment(userID=userID, orderbuyID=orderID, content=content)
        db.session.add(comment)
        db.session.commit()
        commentID = comment.id
        return jsonify({
            'commentID': commentID
        }), 200
    else:
        return jsonify({
            "msg": "openid与userID不同"
        }), 401


# 发起的订单
@api.route('/order/post/list/', methods=['GET'], endpoint='order_list_post')
@User.check
def order_list(openid):
    page = request.args.get('page', 1, type=int)
    pagination = Post2order.query.filter_by(userID=openid).paginate(page, per_page=10, error_out=False)
    items = pagination.items
    orderlist = []
    for item in items:
        kind = item.kind
        if kind == 1:
            orderID = item.orderID
            order = Orderbuy.query.filter_by(id=orderID).first()
            userPicture = []
            postUser = User.query.filter_by(openid=str(order.postID)).first()
            userPicture.append(postUser.headPicture)
            P2order = Pick2order.query.filter_by(kind=1, orderID=orderID).all()
            for u in P2order:
                us = User.query.filter_by(openid=u.userID).first()
                userPicture.append(us.headPicture)
            userPicture = list(set(userPicture))
            while None in userPicture:
                userPicture.remove(None)
            info = {
                "kind": 1,
                'orderbuyID': order.id,
                'heading': order.heading,
                'timeBuy': order.time,
                'location': order.location,
                'numExist': order.numExist,
                'numNeed': order.numNeed,
                'content': order.content,
                "picture": order.picture,
                "userPicture": userPicture
            }
            orderlist.append(info)
        elif kind == 2:
            orderID = item.orderID
            order = Ordercar.query.filter_by(id=orderID).first()
            info = {
                "kind": 2,
                'ordercarID': order.id,
                'heading': order.heading,
                'timeGo': order.time,
                'placeA': order.placeA,
                'placeB': order.placeB,
                'numExist': order.numExist,
                'numNeed': order.numNeed
                }
            orderlist.append(info)
    data = {
        'pageNum': pagination.page,
        'pageMax': pagination.pages,
        'hasNext': pagination.has_next,
        'ordersnum': pagination.total,
        'orderList': orderlist
    }
    return jsonify({
        'data': data
    }), 200

# 加入的订单
@api.route('/order/pick/list/', methods=['GET'], endpoint='order_list_pick')
@User.check
def order_list(openid):
    page = request.args.get('page', 1, type=int)
    pagination = Pick2order.query.filter_by(userID=openid).paginate(page, per_page=10, error_out=False)
    items = pagination.items
    orderlist = []
    for item in items:
        kind = item.kind
        if kind == 1:
            orderID = item.orderID
            order = Orderbuy.query.filter_by(id=orderID).first()
            userPicture = []
            postUser = User.query.filter_by(openid=str(order.postID)).first()
            userPicture.append(postUser.headPicture)
            P2order = Pick2order.query.filter_by(kind=1, orderID=orderID).all()
            for u in P2order:
                us = User.query.filter_by(openid=u.userID).first()
                userPicture.append(us.headPicture)
            userPicture = list(set(userPicture))
            while None in userPicture:
                userPicture.remove(None)
            info = {
                "kind": 1,
                'orderbuyID': order.id,
                'heading': order.heading,
                'timeBuy': order.time,
                'location': order.location,
                'numExist': order.numExist,
                'numNeed': order.numNeed,
                'content': order.content,
                "picture": order.picture,
                "userPicture": userPicture
            }
            orderlist.append(info)
        elif kind == 2:
            orderID = item.orderID
            order = Ordercar.query.filter_by(id=orderID).first()
            info = {
                "kind": 2,
                'ordercarID': order.id,
                'heading': order.heading,
                'timeGo': order.time,
                'placeA': order.placeA,
                'placeB': order.placeB,
                'numExist': order.numExist,
                'numNeed': order.numNeed
                }
            orderlist.append(info)
    data = {
        'pageNum': pagination.page,
        'pageMax': pagination.pages,
        'hasNext': pagination.has_next,
        'ordersnum': pagination.total,
        'orderList': orderlist
    }
    return jsonify({
        'data': data
    }), 200

# 评论过的订单
@api.route('order/comment/list/', methods=['GET'], endpoint='order_list_comment')
@User.check
def order_list(openid):
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.filter_by(userID=openid).paginate(page, per_page=10, error_out=False)
    items = pagination.items
    orderlist = []
    for item in items:
        orderID = item.orderbuyID
        order = Orderbuy.query.filter_by(id=orderID).first()
        userPicture = []
        postUser = User.query.filter_by(openid=str(order.postID)).first()
        userPicture.append(postUser.headPicture)
        P2order = Pick2order.query.filter_by(kind=1, orderID=orderID).all()
        for u in P2order:
            us = User.query.filter_by(openid=u.userID).first()
            userPicture.append(us.headPicture)
        userPicture = list(set(userPicture))
        while None in userPicture:
            userPicture.remove(None)
        
        info = {
            "kind": 1,
            'orderbuyID': order.id,
            'heading': order.heading,
            'timeBuy': order.time,
            'location': order.location,
            'numExist': order.numExist,
            'numNeed': order.numNeed,
            'content': order.content,
            "picture": order.picture,
            "userPicture": userPicture
        }
        orderlist.append(info)
    data = {
        'pageNum': pagination.page,
        'pageMax': pagination.pages,
        'hasNext': pagination.has_next,
        'ordersnum': pagination.total,
        'orderList': orderlist
    }
    return jsonify({
        'data': data
    }), 200

 # if request.method=="GET":
    #     #获取订单信息
    #     order = Ordercar.query.filter_by(id=orderID).first()
    #     info={
    #     'datetime' : order.datetime,
    #     'placeA' : order.placeA,
    #     'placeB' : order.placeB,
    #     'timeGo' : order.time,
    #     'picture' : order.picture,
    #     'heading' : order.heading,
    #     'content' : order.content,
    #     'numNeed': order.numNeed,
    #     'numExist' : order.numExist
    #     }
    #     Post2order=Pick2order.query.filter_by(kind=2, orderID=orderID).all()
    #     userPicture=[]
    #     postUser = User.query.filter_by(openid=order.postID).first()
    #     userPicture.append(postUser.headPicture)
    #     for u in Pick2order:
    #         us=User.query.filter_by(openid=u.userID).first()
    #         userPicture.append(us.headPicture)
    #     userspicture={
    #         'userpictures': userPicture
    #     }
    #     commentss=Comment.query.filter_by(ordercarID=orderID).all()
    #     comments=[]
    #     for c in commentss:
    #         us = User.query.filter_by(openid=c.userID)
    #         x={
    #             'datetime':c.datetime,
    #             'content':c.content,
    #             'headPicture':us.headPicture,
    #             'username':us.username
    #         }
    #         comments.append(x)

    #     data=[info,userPicture,comments]
    #     return jsonify({
    #         'data':data
    #     }),200

# @api.route('/order/comments/car/',methods=['POST'],endpoint='commentCar')
# @User.check
# def comment(openid,orderID):
#     orderID=request.args.get("orderID",-1,type=int)
#     if orderID==-1:
#         return jsonify({
#             "msg":"加上orderID参数"
#         }),402
#     #print("I am here!!!!!!!!!!!!!!!")
#     userID=request.json.get('userID')
#     content=request.json.get('content')
#     #确保准确post
#     if userID==openid:
#         comment=Comment(userID=userID,kind=2,ordercarID=orderID,content=content)
#         db.session.add(comment)
#         db.session.commit()
#         commentID=comment.id
#         return jsonify({
#             'commentID':commentID
#         }),200
#     else:
#         return jsonify({
#             "msg":"openid与userID不同"
# #         })，401       kind=item.kind
#         if kind==1:
#             orderID = item.orderbuyID
#             order=Orderbuy.query.filter_by(id=orderID).first()
#             userPicture=[]
#             postUser = User.query.filter_by(openid=str(order.postID)).first()
#             userPicture.append(postUser.headPicture)
#             P2order=Pick2order.query.filter_by(kind=1, orderID=orderID).all()
#             for u in P2order:
#                 us=User.query.filter_by(openid=u.userID).first()
#                 userPicture.append(us.headPicture)
#             info={
#                 "kind":1,
#                 'orderbuyID': order.id,
#                 'heading': order.heading,
#                 'timeBuy': order.time,
#                 'location': order.location,
#                 'numExist': order.numExist,
#                 'numNeed' : order.numNeed,
#                 'content' : order.content,
#                 "picture" : item.picture,
#                 "userPicture" : userPicture
#             }
#             orderlist.append(info)
#         elif kind==2:
