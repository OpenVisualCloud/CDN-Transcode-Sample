import os, base64
from tornado.web import StaticFileHandler
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_PATH = os.path.dirname(__file__)

set = dict(
    debug = True,
    cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
)

with open('/mysql/mysql-secret', 'r') as f:
    password = base64.b64decode(f.read()).decode('utf-8').split('\n')[0]

# mysql
connect = create_engine("mysql+pymysql://root:" + password + "@"+ "mysql-service" +":3306/Player",
                        echo=True)
DBsession = sessionmaker(bind=connect)
session = DBsession()
Base = declarative_base(connect)
from model.user import *
Base.metadata.create_all()

# redis
import redis
pool = redis.ConnectionPool(host="redis-service")
cursor = redis.Redis(connection_pool=pool)
