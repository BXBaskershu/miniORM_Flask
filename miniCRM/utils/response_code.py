class ErrorCode(object):
    permission_denied = '1001'
    not_login = '1002'
    login_error = '1003'
    params_error = '2001'
    params_lose = '2001'
    username_exist = '3001'
    customer_exist = '3002'
    customer_not_exist = '3003'
    page_error = '4001'


class ErrorMessage(object):
    permission_denied = '无访问权限'
    not_login = '销售未登陆'
    login_error = '登陆失败'
    params_error = '参数错误'
    params_lose = '参数缺失'
    username_exist = '用户名已存在'
    customer_exist = '客户已存在'
    customer_not_exist = '客户不存在'
    page_error = '页数错误'