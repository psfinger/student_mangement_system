import redis


class Config:
    # session
    SECRET_KEY = 'dev'
    # SESSION_TYPE = 'redis'
    # SESSION_REDIS = redis.Redis(host='127.0.0.1', port=6379)
    # sql
    SQLALCHEMY_DATABASE_URI = 'sqlite:///E:/sqlite/studetManagement.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False