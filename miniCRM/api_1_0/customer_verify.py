from . import api
from flask import request, jsonify, current_app, g
from miniCRM.utils.response_code import RET
from miniCRM.models import Customer, CustomerRecord
from miniCRM.utils.commons import login_required
from miniCRM import db


@api.route('/customer', methods=['POST'])
@login_required
def customer_add():
    """客户录入"""

    customer_data = request.get_json()

    if not customer_data:
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    name = customer_data.get('name')
    telephone = customer_data.get('telephone')
    detail = customer_data.get('detail')
    salesman_id = g.salesman_id

    if not all([name, telephone, detail, salesman_id]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数缺失')

    try:
        customer = Customer.query.filter_by(telephone=telephone).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询客户数据异常')
    else:
        if customer:
            return jsonify(errno=RET.DATAEXIST, errmsg='客户已存在')

    customer = Customer(name=name, telephone=telephone, detail=detail, salesman_id=salesman_id)

    try:
        db.session.add(customer)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='录入客户信息异常')

    return jsonify(data=customer.to_dict())


@api.route('/customer/<int:customer_id>', methods=['PUT'])
@login_required
def customer_update(customer_id):
    """修改客户信息"""

    customer_data = request.get_json()

    if not customer_data:
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    name = customer_data.get('name')
    telephone = customer_data.get('telephone')

    if not all([name, telephone]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数缺失')

    try:
        Customer.query.filter_by(id=str(customer_id)).update({'name': name, 'telephone': telephone})
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='修改客户信息失败')

    return jsonify(data={'name': name, 'telephone': telephone})


@api.route('/customer_record/<int:customer_id>', methods=['POST'])
@login_required
def customer_record_add(customer_id):
    """跟进客户小记"""

    customer_record_data = request.get_json()

    if not customer_record_data:
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    content = customer_record_data.get('content')
    salesman_id = g.salesman_id

    if not all([content, salesman_id, customer_id]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数缺失')

    customer_record = CustomerRecord(content=content, customer_id=customer_id, salesman_id=salesman_id)

    try:
        db.session.add(customer_record)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='客户跟进记录异常')

    return jsonify(data=customer_record.to_dict())
