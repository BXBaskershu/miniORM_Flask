from . import api
from miniCRM.libs.response import Response
from .functions import *


@api.route('/customer/<int:customer_id>', methods=['GET'])
def customer_info(customer_id):
    """获取客户信息"""
    try:
        ret = get_customer_info(customer_id)
        return Response.success_with_data('data', ret)
    except Exception as e:
        return Response.error(str(e))


@api.route('/customers/<int:salesman_id>', methods=['GET'])
def get_customer_list(salesman_id):
    """获取客户列表"""
    try:
        ret = get_customer_basic_list(salesman_id)
        return Response.success_with_data('data', ret)
    except Exception as e:
        return Response.error(str(e))

