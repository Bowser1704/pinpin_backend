#coding=utf-8

import re
import requests
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from config import config

def try_login(username,password):
    s = requests.Session()
    headers = {
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"
    }
    s.get("https://account.ccnu.edu.cn/cas/login",headers=headers)
    res = s.get("https://account.ccnu.edu.cn/cas/login",headers=headers)
    execution = re.search('execution" value="(.+?)"', res.text).group(1)
    lt = re.search('lt" value="(.+?)"', res.text).group(1)
    data = {
    "username" : username,
    "password": password,
    "execution": execution,
    "lt": lt,
    "_eventId": "submit",
    "submit": "登录"
    }
    res = s.post("https://account.ccnu.edu.cn/cas/login", data=data,headers=headers)
    try:
        cookie=res.headers['Set-Cookie']
        if "CASTGC" in cookie:
            return True
    except:
        return False

def get_id(token):
    s = Serializer(config['config'].SECRET_KEY)
    try:
        data = s.loads(token)
    except:
        return False
    return data.get('openid')
