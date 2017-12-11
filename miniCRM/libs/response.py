from flask import make_response, jsonify
from miniCRM.utils.response_code import ErrorCode,ErrorMessage


class Response(object):

    @staticmethod
    def construct_response(content):
        resp = make_response(jsonify(content))
        return resp

    @staticmethod
    def error(errmsg, desc=''):
        content = {
            'status': 0,
            'msg': errmsg,
            'desc': desc
        }
        return Response.construct_response(content)

    @staticmethod
    def success(desc=''):
        content = {
            'status': 100,
            'msg': 'success',
            'desc': desc
        }
        return Response.construct_response(content)

    @staticmethod
    def success_with_data(return_key, return_val, desc=''):
        content = {
            'status': 101,
            'msg': 'success',
            'desc': desc,
            return_key: return_val
        }
        return Response.construct_response(content)

    @staticmethod
    def permission_denied():
        return Response.error(ErrorCode.permission_denied, ErrorMessage.permission_denied)
