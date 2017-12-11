from flask import Blueprint, request

api = Blueprint('api', __name__)

from . import customer_show, customer_verify, salesman_verify


@api.after_request
def after_request(response):
    """设置默认的响应报文格式为application/json"""
    if response.headers.get("Content-Type").startswith("text"):
        response.headers["Content-Type"] = "application/json"
    response.headers.add('Access-Control-Allow-Origin', '*')
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response


