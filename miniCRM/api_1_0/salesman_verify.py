from . import api
from flask import request, jsonify, current_app, session
from miniCRM.utils.db_utils import commit
from miniCRM.models import Salesman
from miniCRM import db
from miniCRM.libs.response import Response
from miniCRM.auth import authentucate, salesman_by_username


@api.route('/login', methods=['POST'])
def login():

    salesman_data = request.get_json()

    if not salesman_data:
        return Response.params_error()

    username = salesman_data.get('username')
    password = salesman_data.get('password')

    if not username:
        return Response.params_lose('username')

    if not password:
        return Response.params_lose('password')

    if authentucate(username, password):
        return Response.success()
    else:
        return Response.login_error()


@api.route('/register', methods=['POST'])
@commit
def register():

    salesman_data = request.get_json()

    if not salesman_data:
        return Response.params_error()

    username = salesman_data.get('username')
    password = salesman_data.get('password')
    name = salesman_data.get('name')
    job_code = salesman_data.get('job_code')

    if not username:
        return Response.params_lose('username')

    if not password:
        return Response.params_lose('password')

    if not name:
        return Response.params_lose('name')

    if not job_code:
        return Response.params_lose('job_code')

    salesman = salesman_by_username(username)

    if salesman:
        return Response.username_exist()

    salesman = Salesman(username=username, name=name, job_code=job_code)
    salesman.set_password = password

    db.session.add(salesman)

    session['id'] = salesman.id
    session['username'] = username

    return Response.success()
