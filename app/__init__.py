#coding=utf-8

'''
from ccnupp_back import manage
'''
import os
from flask import Flask
from flask_script import Manager,Shell
#from app.api import api
import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config

db = SQLAlchemy()
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    #db = SQLAlchemy(app)
    with app.app_context():
        db.init_app(app)
    db.init_app(app)
    #实例化迁移对象时传入 app，db
    migrate=Migrate(app,db)
    manager=Manager(app)

    from .api import api
    app.register_blueprint(api, url_prefix='/api/v1')
    # api = Api(app, version='1.0', title='ccnupp API',
    # description='A simple API',
    # )
    return app

# if __name__ == "__main__":
app = create_app('config')
app.app_context().push()
# db.drop_all()
db.create_all()