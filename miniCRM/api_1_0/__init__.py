from flask import Blueprint

api = Blueprint('api', __name__)

from . import customer_show, customer_verify, salesman_verify


@api.after_request
def after_request(response):
    """设置默认的响应报文格式为application/json"""
    if response.headers.get("Content-Type").startswith("text"):
        response.headers["Content-Type"] = "application/json"
    return response
