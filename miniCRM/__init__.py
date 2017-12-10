import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_session import Session
from config import config, Config
from miniCRM.utils.commons import RegexConverter


db = SQLAlchemy()
SESSION_REDIS = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

# csrf = CSRFProtect()


# 创建应用程序实例
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.url_map.converters["regex"] = RegexConverter
    # csrf.init_app(app)

    Session(app)

    db.init_app(app)

    # 使用蓝图
    from .api_1_0 import api
    app.register_blueprint(api, url_prefix="/api/v1.0")

    from .web_page import html as html_blueprint
    app.register_blueprint(html_blueprint)

    return app
