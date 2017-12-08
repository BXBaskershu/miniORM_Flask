from . import api
from flask import request, jsonify, current_app, session
from miniCRM.utils.response_code import RET
from miniCRM.models import Salesman
from miniCRM import db


@api.route('/login', methods=['POST'])
def login():

    salesman_data = request.get_json()

    if not salesman_data:
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    username = salesman_data.get('username')
    password = salesman_data.get('password')

    if not all([username, password]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数缺失')
    try:
        salesman = Salesman.query.filter_by(username=username).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='获取用户信息异常')
    if salesman is None or not salesman.check_password(password):
        return jsonify(errno=RET.DATAERR, errmsg='用户名或密码错误')

    session['id'] = salesman.id
    session['username'] = username

    return jsonify(data={'id': salesman.id})


@api.route('/register', methods=['POST'])
def register():

    salesman_data = request.get_json()

    if not salesman_data:
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    username = salesman_data.get('username')
    password = salesman_data.get('password')
    name = salesman_data.get('name')
    job_code = salesman_data.get('job_code')

    if not all([username, password, name, job_code]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数缺失')

    try:
        salesman = Salesman.query.filter_by(username=username).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据异常')
    else:
        if salesman:
            return jsonify(errno=RET.DATAEXIST, errmsg='用户名已存在')

    salesman = Salesman(username=username, name=name, job_code=job_code)
    salesman.password = password

    try:
        db.session.add(salesman)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存用户信息异常')

    session['id'] = salesman.id
    session['username'] = username

    return jsonify(data=salesman.to_dict())
