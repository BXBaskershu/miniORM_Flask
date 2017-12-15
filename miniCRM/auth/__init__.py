import jwt, datetime
from miniCRM.models import Salesman
from miniCRM import config
from config import Config
from miniCRM.utils.response_code import ErrorCode, ErrorMessage
from flask import current_app, g


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
        try:
            auth_header = request.headers.get('Authorization')
            if auth_header:
                auth_tokenArr = auth_header.split(" ")
                if auth_tokenArr[0] != 'JWT' or len(auth_tokenArr) != 2:
                    raise ValueError(ErrorCode.request_header_error, ErrorMessage.request_header_error)
                else:
                    auth_token = auth_tokenArr[1]
                    payload = self.decode_auth_token(auth_token)
                    if g.salesman_id == payload['data']['id']:
                        return True
                    else:
                        raise ValueError(ErrorCode.login_error, ErrorMessage.login_error)
            else:
                raise ValueError(ErrorCode.login_error, ErrorMessage.login_error)
        except Exception as e:
            current_app.logger.info(e)
            raise e

