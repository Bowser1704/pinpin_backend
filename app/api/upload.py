#coding=utf-8


import requests
import os
import simplejson as json
from flask import jsonify, request
import datetime
import qiniu.config
import oss2
import base64

from qiniu import Auth, put_file, etag, urlsafe_base64_encode
from . import api
from .. import db
from ..login import get_id
from ..models import Comment, Orderbuy, Ordercar, User,Pick2order,Post2order


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

#上传图片
@api.route('/order/image/',methods=['POST'])
@User.check
def image(openid):
    image = request.files['image']
    imagename = str(openid)+str(datetime.datetime.utcnow())+'.'+str(image.filename.rsplit('.',1)[1])
    if allowed_file(image.filename):    
        key = imagename
        access_id = os.environ.get('AL_ACCESS_ID')
        print('0----->'+str(access_id))
        access_key = os.environ.get('AL_ACCESS_KEY')
        print('0----->'+str(access_key))
        auth = oss2.Auth(access_id,access_key)
        endpoint = "http://oss-cn-shanghai.aliyuncs.com"
        bucket = oss2.Bucket(auth,endpoint,'ccnupp')
        
        path = os.path.join(os.getcwd(),imagename)
        image.save(path)
        a=bucket.put_object_from_file(imagename,path)
        os.remove(path)
        url = 'https://ccnupp.oss-cn-shanghai.aliyuncs.com/'
        if a:
            image_url=url + str(imagename)
            return jsonify({
                "image_url":image_url
            }),200
    else:
        return jsonify({
            "msg":"extensions error"
        }),403