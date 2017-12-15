from . import api
from flask import request, jsonify, current_app, session
from miniCRM.models import Salesman
from miniCRM.libs.response import Response
from miniCRM.auth import Auth
from .functions import *


@api.route('/login', methods=['POST'])
def login():
    try:
        token = salesman_login()
        if token:
            return Response.success_with_data('data', token)
    except Exception as e:
        return Response.error(str(e))


@api.route('/register', methods=['POST'])
def register():
    try:
        if salesman_register():
            return Response.success()
    except Exception as e:
        return Response.error(str(e))

