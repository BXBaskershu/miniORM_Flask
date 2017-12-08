import functools
from flask import g, session, jsonify
from werkzeug.routing import BaseConverter
from .response_code import RET
from flask import request, jsonify, current_app


class RegexConverter(BaseConverter):
    """在路由中使用正则表达式进行提取参数的转换工具"""
    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]


def login_required(func):
    """要求销售登录的验证装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        salesman_id = session.get("salesman_id")
        if salesman_id is None:
            return jsonify(errno=RET.SESSIONERR, errmsg="销售人员未登录")
        else:
            g.salesman_id = salesman_id
            return func(*args, **kwargs)
    return wrapper


def page_str_to_int():
    page_str = request.args.get('p', '1')
    try:
        return int(page_str)
    except Exception as e:
        current_app.logger.error(e)
        return 0
