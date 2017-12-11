from . import api
from flask import request, jsonify, current_app, g
from miniCRM.models import Customer, CustomerRecord
from miniCRM import db
from miniCRM.libs.response import Response


@api.route('/customer', methods=['POST'])
def customer_add():
    """客户录入"""

    customer_data = request.get_json()
    if not customer_data:
        return Response.params_error()

    name = customer_data.get('name')
    telephone = customer_data.get('telephone')
    detail = customer_data.get('detail')
    # salesman_id = g.salesman_id
    salesman_id = 1

    if not name:
        return Response.params_lose('name')
    if not telephone:
        return Response.params_lose('telephone')
    if not detail:
        return Response.params_lose('detail')

    customer = Customer.get_from_telephone(Customer, telephone)
    if customer:
        return Response.customer_exist()

    customer = Customer(name=name, telephone=telephone, detail=detail, salesman_id=salesman_id)
    Customer.add(customer)

    return Response.success()


@api.route('/customer/<int:customer_id>', methods=['PUT'])
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

    customer = Customer.get_from_telephone(telephone)
    if customer:
        return Response.customer_exist()

    customer = Customer.get_from_id(customer_id)
    customer.name = name
    customer.telephone = telephone
    customer.update()

    return Response.success()


@api.route('/customer_record/<int:customer_id>', methods=['POST'])
def customer_record_add(customer_id):
    """跟进客户小记"""
    customer_record_data = request.get_json()
    if not customer_record_data:
        return Response.params_error()

    content = customer_record_data.get('content')
    # salesman_id = g.salesman_id
    salesman_id=1

    if not content:
        return Response.params_lose('content')

    customer_record = CustomerRecord(content=content, customer_id=customer_id, salesman_id=salesman_id)
    CustomerRecord.add(customer_record)

    return Response.success()
