from . import api
from miniCRM.libs.response import Response
from .functions import *


@api.route('/customer', methods=['POST'])
def customer_add():
    """客户录入"""
    try:
        if customer_data_save():
            return Response.success()
    except Exception as e:
        return Response.error(str(e))


@api.route('/customer/<int:customer_id>', methods=['PUT'])
def customer_update(customer_id):
    """修改客户信息"""
    try:
        if customer_data_update(customer_id):
            return Response.success()
    except Exception as e:
        return Response.error(str(e))


@api.route('/customer_record/<int:customer_id>', methods=['POST'])
def customer_record_add(customer_id):
    """跟进客户小记"""
    try:
        if customer_record_save(customer_id):
            return Response.success()
    except Exception as e:
        return Response.error(str(e))
