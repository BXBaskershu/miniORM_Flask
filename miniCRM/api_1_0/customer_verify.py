from . import api
from flask import request, jsonify, current_app, g
from miniCRM.models import Customer, CustomerRecord
from miniCRM.utils.commons import login_required
from miniCRM import db
from miniCRM.utils.db_utils import commit
from miniCRM.libs.response import Response


@api.route('/customer', methods=['POST'])
@login_required
@commit
def customer_add():
    """客户录入"""
    customer_data = request.get_json()
    if not customer_data:
        return Response.params_error()

    name = customer_data.get('name')
    telephone = customer_data.get('telephone')
    detail = customer_data.get('detail')
    salesman_id = g.salesman_id

    if not name:
        return Response.params_lose('name')
    if not telephone:
        return Response.params_lose('telephone')
    if not detail:
        return Response.params_lose('detail')

    customer = Customer.query.filter_by(telephone=telephone).first()
    if customer:
        return Response.customer_exist()

    customer = Customer(name=name, telephone=telephone, detail=detail, salesman_id=salesman_id)
    db.session.add(customer)

    return Response.success()


@api.route('/customer/<int:customer_id>', methods=['PUT'])
@login_required
@commit
def customer_update(customer_id):
    """修改客户信息"""
    customer_data = request.get_json()
    if not customer_data:
        return Response.params_error()

    name = customer_data.get('name')
    telephone = customer_data.get('telephone')
    if not name:
        return Response.params_lose('name')
    if not telephone:
        return Response.params_lose('telephone')

    customer = Customer.query.filter_by(telephone=telephone).first()
    if customer:
        return Response.customer_exist()

    customer = Customer(id=customer_id, name=name, telephone=telephone)
    db.session.merge(customer)

    return Response.success()


@api.route('/customer_record/<int:customer_id>', methods=['POST'])
@login_required
@commit
def customer_record_add(customer_id):
    """跟进客户小记"""
    customer_record_data = request.get_json()
    if not customer_record_data:
        return Response.params_error()

    content = customer_record_data.get('content')
    salesman_id = g.salesman_id
    if not content:
        return Response.params_lose('content')

    customer_record = CustomerRecord(content=content, customer_id=customer_id, salesman_id=salesman_id)
    db.session.add(customer_record)

    return Response.success()
