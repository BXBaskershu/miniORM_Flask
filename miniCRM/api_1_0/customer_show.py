import json
from . import api
from flask import request, current_app
from miniCRM.models import Customer, CustomerRecord
from miniCRM.utils.commons import page_str_to_int, paging, save_customer_to_redis
from miniCRM import redis_store, constants
from miniCRM.libs.response import Response


@api.route('/customer/<int:customer_id>', methods=['GET'])
def customer_info(customer_id):
    """获取客户信息"""

    if not customer_id:
        return Response.params_error()

    page = page_str_to_int()
    if not page:
        return Response.page_error()

    is_basic = request.args.get('is_basic', 'false')

    # 查看redis中是否存在客户信息
    ret = redis_store.get('customer_info_%s' % customer_id)

    if ret and (is_basic == "true"):
        current_app.logger.info('从redis中获取到客户信息')
        return Response.success_with_data('data', ret.decode())

    # mysql中查询
    customer = Customer.get_from_id(customer_id)
    if customer is None:
        return Response.customer_not_exist()

    customer_data = customer.to_basic_dict()

    # 序列化数据,转成json格式,存入缓存中
    save_customer_to_redis(customer_id, customer_data)

    if is_basic == "true":
        return Response.success_with_data('data', customer.to_basic_dict())

    customer_data = customer.to_dict()

    # 追加客户小记分页
    customer_records = CustomerRecord.records_all(customer_id)

    customer_records_page, customer_records_list, total_page = paging(
        customer_records, page, constants.CUSTOMER_LIST_PAGE_CAPACITY)

    customer_records_dict_list = [i.to_basic_dict() for i in customer_records_list]

    data = {'customers': customer_data, 'customer_records_list': customer_records_dict_list,
            'total_page': total_page, 'current_page': page}
    return Response.success_with_data('data', data)


@api.route('/customers/<int:salesman_id>', methods=['GET'])
def get_customer_list(salesman_id):
    """获取客户列表"""

    page = page_str_to_int()
    if not page:
        return Response.page_error()

    # 所有客户
    if salesman_id == 0:
        customers = Customer.get_all()
    # 根据销售id查询对应客户
    else:
        customers = Customer.qget_one_all(salesman_id)

    customers_page, customer_list, total_page = paging(
        customers, page, constants.CUSTOMER_LIST_PAGE_CAPACITY)

    customer_dict_list = [i.to_basic_dict() for i in customer_list]

    data = {'customers': customer_dict_list, 'total_page': total_page, 'current_page': page}
    return Response.success_with_data('data', data)
