import datetime
import json
from . import api
from flask import request, jsonify, current_app, g
from miniCRM.utils.response_code import RET
from miniCRM.models import Customer, CustomerRecord
from miniCRM.utils.commons import login_required
from miniCRM import redis_store, constants, db


@api.route('/customer/<int:customer_id>', methods=['GET'])
@login_required
def customer_detail(customer_id):
    """获取客户详情信息"""

    if not customer_id:
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    # 查看redis中是否存在客户信息
    try:
        ret = redis_store.get('customer_info_%s' % customer_id)
    except Exception as e:
        current_app.logger.error(e)
        ret = None

    if ret:
        current_app.logger.info('从redis中获取到客户基本信息')
        return '{"errno":0,"errmsg":"OK","data":{"customer_id":%s,"customer":%s}}' % (customer_id, ret)

    # mysql中查询
    try:
        customer = Customer.query.get(customer_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询客户信息异常')

    if not customer:
        return jsonify(errno=RET.NODATA, errmsg='无客户数据')

    try:
        customer_records = CustomerRecord.query.filter(customer_id=customer_id).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询客户跟进记录数据异常')

    try:
        customer_data = customer.to_dict()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg='客户数据格式错误')

    try:
        customer_records_data = customer_records.to_dict()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg='客户跟进数据格式错误')

    customer_all_data = customer_data + customer_records_data

    # 序列化数据,转成json格式,存入缓存中
    json_customer = json.dumps(customer_all_data)

    try:
        redis_store.setex('customer_info_%s' % customer_id, constants.CUSTOMER_DETAIL_REDIS_EXPIRE_SECOND, json_customer)
    except Exception as e:
        current_app.logger.error(e)

    return "{'errno':0,'errmsg':'OK','data':{'customer_id':%s, 'customer':%s}}" % (customer_id, json_customer)


@api.route('/customers', methods=['GET'])
@login_required
def get_customer_list():
    """获取所有客户列表"""

    # salesman_id = g.salesman_id
    page = request.args.get('p', '1')

    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg='页数格式化错误')

    try:
        customers = Customer.query.all().order_by(Customer.created_time.desc())
        customers_page = customers.paginate(page, constants.CUSTOMER_LIST_PAGE_CAPACITY, False)

        customer_list = customers_page.items

        total_page = customers_page.pages

        # 获取客户的基本信息
        customer_dict_list = []
        for customer in customer_list:
            customer_dict_list.append(customer.to_basic_dict())
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询客户列表信息异常')

    return "{'errno': 0, 'errmsg': 'OK', 'data': {'customers': %s, 'total_page': %s, 'current_page': %s}}" \
           % (customer_dict_list, total_page, page)