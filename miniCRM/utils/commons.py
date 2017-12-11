import functools
from flask import g, session, request, current_app
from werkzeug.routing import BaseConverter
from miniCRM.libs.response import Response
from miniCRM import redis_store, constants
import json


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
            return Response.not_login()
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
        raise ValueError


# 分页
def paging(data_obj, page, page_capacity):
    data_page = data_obj.paginate(page, page_capacity, False)
    data_list = data_page.items
    total_page = data_page.pages
    return data_page, data_list, total_page


def save_customer_to_redis(customer_id, customer_data):
    json_customer = json.dumps(customer_data)
    redis_store.setex('customer_info_%s' % customer_id, constants.CUSTOMER_DETAIL_REDIS_EXPIRE_SECOND,
                      json_customer)

