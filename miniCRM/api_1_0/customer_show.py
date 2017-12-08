import json
from . import api
from flask import request, jsonify, current_app
from miniCRM.utils.response_code import RET
from miniCRM.models import Customer, CustomerRecord
from miniCRM.utils.commons import login_required, page_str_to_int
from miniCRM import redis_store, constants


@api.route('/customer/<int:customer_id>', methods=['GET'])
@login_required
def customer_info(customer_id):
    """获取客户信息"""

    if not customer_id:
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    page = page_str_to_int()
    if page == 0:
        return jsonify(errno=RET.DATAERR, errmsg='页数格式化错误')

    is_basic = request.args.get('is_basic', 'false')

    # 查看redis中是否存在客户信息
    try:
        ret = redis_store.get('customer_info_%s' % customer_id)
    except Exception as e:
        current_app.logger.error(e)
        ret = None

    if ret and (is_basic == "true"):
        current_app.logger.info('从redis中获取到客户信息')
        return jsonify(errno=RET.OK, errmsg='OK', data=str(ret))

    # mysql中查询
    try:
        customer = Customer.query.get(customer_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='获取客户信息异常')

    if customer is None:
        return jsonify(errno=RET.NODATA, errmsg='无效操作')

    try:
        customer_data = customer.to_basic_dict()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg='客户数据格式错误')

    # 序列化数据,转成json格式,存入缓存中
    json_customer = json.dumps(customer_data)

    try:
        redis_store.setex('customer_info_%s' % customer_id, constants.CUSTOMER_DETAIL_REDIS_EXPIRE_SECOND, json_customer)
    except Exception as e:
        current_app.logger.error(e)

    if is_basic == "true":
        return jsonify(errno=RET.OK, errmsg='OK', data=customer.to_basic_dict())

    customer_data = customer.to_dict()
    try:
        # 追加客户小记分页面
        customer_records = CustomerRecord.query.filter_by(customer_id=customer_id).order_by(CustomerRecord.created_time.desc())

        customer_records_page = customer_records.paginate(page, constants.CUSTOMER_LIST_PAGE_CAPACITY, False)
        customer_records_list = customer_records_page.items
        total_page = customer_records_page.pages

        customer_records_dict_list = []
        for customer_record in customer_records_list:
            customer_records_dict_list.append(customer_record.to_dict())
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询跟进客户小记信息异常')

    data = {'data': {'customers': customer_data, 'customer_records_list': customer_records_dict_list,
                     'total_page': total_page, 'current_page': page}}
    return jsonify(data)


@api.route('/customers/<int:salesman_id>', methods=['GET'])
@login_required
def get_customer_list(salesman_id):
    """获取客户列表"""

    page = page_str_to_int()
    if page == 0:
        return jsonify(errno=RET.DATAERR, errmsg='页数格式化错误')

    try:
        # 所有客户
        if salesman_id == 0:
            customers = Customer.query.order_by(Customer.created_time.desc())
        # 根据i销售d查询对应客户
        else:
            customers = Customer.query.filter_by(salesman_id=salesman_id).order_by(Customer.created_time.desc())

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

    data = {'data': {'customers': customer_dict_list, 'total_page': total_page, 'current_page': page}}
    return jsonify(data)
