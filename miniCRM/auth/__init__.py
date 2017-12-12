import jwt, datetime, time
from miniCRM.models import Salesman
from miniCRM import config
from miniCRM.libs.response import Response
from config import Config
from miniCRM.utils.response_code import ErrorCode, ErrorMessage


class Auth(object):

    @staticmethod
    def encode_auth_token(salesman_id, login_time):
        """生成认证Token"""
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=10),
                'iat': datetime.datetime.utcnow(),
                'iss': 'ban',
                'data': {
                    'id': salesman_id,
                    'login_time': login_time
                }
            }
            return jwt.encode(
                payload,
                Config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """验证Token"""
        try:
            # 取消过期时间验证
            payload = jwt.decode(auth_token, config.SECRET_KEY, options={'verify_exp': False})
            if 'id' in payload['data']:
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            raise jwt.ExpiredSignatureError(ErrorCode.login_error, ErrorMessage.login_error)
        except jwt.InvalidTokenError:
            raise jwt.ExpiredSignatureError(ErrorCode.login_error, ErrorMessage.login_error)


    def identify(self, request):
        """鉴权"""
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_tokenArr = auth_header.split(" ")
            if auth_tokenArr[0] != 'JWT' or len(auth_tokenArr) != 2:
                result = Response.request_header_error()
            else:
                auth_token = auth_tokenArr[1]
                payload = self.decode_auth_token(auth_token)
                if not isinstance(payload, str):
                    salesman = Salesman.get(Salesman, payload['data']['id'])
                    if salesman is None:
                        result = Response.not_login()
                    else:
                        if (salesman.login_time == payload['data']['login_time']):
                            result = Response.success_with_data("salesman_id", salesman.salesman_id)
                        else:
                            result = Response.false_return()
                else:
                    result = Response.false_return()
        else:
            result = Response.false_return()
        return result
