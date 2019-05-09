import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY=os.getenv('SECRET_KEY') or "you naadsadafs"
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL')or\
        'sqlite:///'+os.path.join(basedir,'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS  = False
    MAX_CONTENT_LENGTH = 3*1024*1024
    # UPLOAD_FOLDER = os.getcwd()

class Testconfig(Config):
    TESTING = True
    SERVER_NAME = '127.0.0.1:5000'
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL')or\
        'sqlite:///'+os.path.join(basedir,'test.db')


config = {
    'config':Config,
    'testconfig':Testconfig
}
