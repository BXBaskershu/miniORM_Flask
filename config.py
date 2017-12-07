import logging
from logging.handlers import RotatingFileHandler


class Config:
    """基本配置参数"""
    SECRET_KEY = "TQ6uZxn+SLqiLgVimX838/VplIsLbEP5jV7vvZ+Ohqw="

    # mysql配置
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/mini_crm_flask"  # 数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # 追踪数据库的修改行为，如果不设置会报警告，不影响代码的执行

    # redis参数
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # flask-session
    SESSION_TYPE = "redis"
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = 86400

    # 日志配置
    logging.basicConfig(level=logging.DEBUG)
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    file_log_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_log_handler)


class DevelopmentConfig(Config):
    """开发模式的配置参数"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境的配置参数"""
    pass


config = {
    "development": DevelopmentConfig,  # 开发模式
    "production": ProductionConfig  # 生产/线上模式
}