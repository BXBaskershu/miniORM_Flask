from flask import make_response, jsonify
from miniCRM.utils.response_code import ErrorCode,ErrorMessage


class Response(object):

    @staticmethod
    def construct_response(content):
        resp = make_response(jsonify(content))
        return resp

    @staticmethod
    def error(error_code,  errmsg, desc=''):
        content = {
            'status': 1,
            'error_code': error_code,
            'msg': errmsg,
            'desc': desc
        }
        return Response.construct_response(content)

    @staticmethod
    def success(desc=''):
        content = {
            'status': 000,
            'msg': 'success',
            'desc': desc
        }
        return Response.construct_response(content)

    @staticmethod
    def success_with_data(return_key, return_val, desc=''):
        content = {
            'status': 1,
            'msg': 'success',
            'desc': desc,
            return_key: return_val
        }
        return Response.construct_response(content)

    @staticmethod
    def permission_denied():
        return Response.error(ErrorCode.permission_denied, ErrorMessage.permission_denied)

    @staticmethod
    def params_error():
        return Response.error(ErrorCode.params_error, ErrorMessage.params_error)

    @staticmethod
    def params_lose(*args):
        return Response.error(ErrorCode.params_lose, '{}:{}'.format(ErrorMessage.params_lose, *args))

    @staticmethod
    def not_login():
        return Response.error(ErrorCode.not_login, ErrorMessage.not_login)

    @staticmethod
    def login_error():
        return Response.error(ErrorCode.login_error, ErrorMessage.login_error)

    @staticmethod
    def username_exist():
        return Response.error(ErrorCode.username_exist, ErrorMessage.username_exist)

    @staticmethod
    def customer_exist():
        return Response.error(ErrorCode.customer_exist, ErrorMessage.customer_exist)

    @staticmethod
    def page_error():
        return Response.error(ErrorCode.page_error, ErrorMessage.page_error)

    @staticmethod
    def customer_not_exist():
        return Response.error(ErrorCode.customer_not_exist, ErrorMessage.customer_not_exist)

