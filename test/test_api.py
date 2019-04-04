#coding=utf-8

import unittest
import json
from flask import current_app,url_for,jsonify
from app import create_app,db
from app.models import User,Post2order,Pick2order,Orderbuy,Ordercar
from functools import wraps
from io import StringIO


class APItest(unittest.TestCase):
    def setUp(self):
        app=create_app('testconfig')
        # app.app_context().push()
        self.app_context=app.app_context()
        self.app_context.push()
        #这一步十分重要，这样才会有下文，才会链接到URI
        db.drop_all()
        db.create_all()
        self.client=app.test_client()

        us = User(openid='1',stNum='2018212576')
        x={
        "kind":2,
        "location":"wdq",
        "timeBuy":",sd",
        "numNeed":3,
        "heading":"dqw",
        "content":"asd",
        "tel":"14796825550",
        "wechat":"xianshi",
        "postID":"1"
        }
        od = Orderbuy()
        # for key,value in x.items():
        #     od.key=value
        od.numNeed=3
        od.numExist=1
        db.session.add(us)
        db.session.add(od)
        db.session.commit()
        print("------>{}".format(od.id))


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exist(self):
        self.assertFalse(current_app is None)

    TOKEN=1
    headers=1
    def test_auth_login(self):
        data=json.dumps({
                "stNum":"2018212576",
                "password":"0"
            })
        a={
            "Content-Type":"application/json",
            "openid":1
        }
        # print("--:", url_for('api.login',_external=True))
        res=self.client.post(url_for('api.login',_external=True),data=data,headers=a)
        data=res.get_json()
        global TOKEN
        TOKEN=data['token']
        global headers
        headers={
            "token":TOKEN,
            "Accept":"application/json",
            "Content-Type":"application/json",
            "openid":"1"
        }
        #print(TOKEN)
        self.assertEqual(res.status_code,200)
        self.assertIn('token',data)
    
    
    
    def test_get_user_info(self):
        res=self.client.get(url_for('api.user_info', _external=True),headers=headers)
        data=res.get_json()
        self.assertEqual(res.status_code,200)
        self.assertIn('info',data)
    
   
    def test_put_user_info(self):
        data={
            "username":"Bowser",
            "headPicture":"aap",
            "tel":"2018212576",
            "wechat":"xianshi",
            "qq":"896379346"
            }
        data=json.dumps(data)
        res=self.client.put(url_for('api.user_info',_external=True),data=data,headers=headers)
        self.assertEqual(res.status_code,200)


   
    def test_order_post(self):
        data=json.dumps({
            "kind":1,
            "location":"wdq",
            "timeBuy":",sd",
            "numNeed":3,
            "heading":"dqw",
            "content":"asd",
            "tel":"14796825550",
            "wechat":"xianshi"
        })
        res = self.client.post(url_for('api.order_buy',_external=True),headers=headers,data=data)
        data = res.get_json()
        # print('jqkljewqlke'+str(data['orderID'])
        #print("order id is {}".format(data['orderID']))
        self.assertEqual(res.status_code,200)
        self.assertIn('orderID',data)

   
    def test_order_get(self):
        res = self.client.get(url_for('api.order_buy',orderID=1,_external=True),headers=headers)
        data = res.get_json()
        print(data)
        self.assertEqual(res.status_code,200)
        self.assertIn('data',data)
    
   
    def test_order_pick(self):
        data = json.dumps({
            "userID":"1"
        })
        res = self.client.post(url_for('api.order_buy',orderID=1,_external=True),data=data,headers=headers)
        data = res.get_json()
        self.assertEqual(res.status_code,200)
        self.assertIn('way',data)


   
    def test_comment_post(self):
        #print(url_for('api.comment',orderID=1,_external=True))
        data=json.dumps({
            "userID":1,
            "content":"weqwrqrwq"
        })
        res = self.client.post(url_for('api.commentBuy',orderID=1,_external=True),headers=headers,data=data)
        data = res.get_json()
        self.assertEqual(res.status_code,200)
        self.assertIn('commentID',data)


    
    def test_order_get_list(self):
        res = self.client.get(url_for("api.order_list",kind=1,page=1,_external=True),headers=headers)
        data = res.get_json()
        self.assertEqual(res.status_code,200)
        self.assertIn('data',data)

    def test_list_post(self):
        res = self.client.get(url_for('api.order_list_post',_external=True),headers=headers)
        data = res.get_json()
        self.assertEqual(res.status_code,200)
        self.assertIn('data',data)

   
    def test_list_pick(self):
        res = self.client.get(url_for('api.order_list_pick',_external=True),headers=headers)
        data = res.get_json()
        self.assertEqual(res.status_code,200)
        self.assertIn('data',data)    

   
    def test_list_comment(self):
        res = self.client.get(url_for('api.order_list_comment',_external=True),headers=headers)
        data = res.get_json()
        
        self.assertIn('data',data)

    

    