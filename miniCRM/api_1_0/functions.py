from miniCRM.utils.response_code import ErrorCode, ErrorMessage
from miniCRM.models import Customer, CustomerRecord, Salesman
from miniCRM.utils.commons import page_str_to_int, paging
from flask import request, current_app
from miniCRM import redis_store, constants
import json
import time
from miniCRM.auth import Auth


def get_request_data():
    data = request.get_json()
    if not data:
        raise ValueError(ErrorCode.params_error, ErrorMessage.params_error)
    else:
        return data


def get_customer_obj_by_telephone(telephone):
    customer = Customer.get_from_telephone(telephone)
    if customer:
        raise ValueError(ErrorCode.customer_exist, ErrorMessage.customer_exist)
    else:
        return customer


def get_customer_from_id(customer_id):
    customer = Customer.get_from_id(customer_id)
    if customer is None:
        raise ValueError(ErrorCode.customer_not_exist, ErrorMessage.customer_not_exist)
    else:
        return customer


def get_salesman_from_id(salesman_id):
    salesman = Salesman.get_from_id(salesman_id)
    if salesman is None:
        raise ValueError(ErrorCode.customer_not_exist, ErrorMessage.customer_not_exist)
    else:
        return salesman


def get_salesman_from_username(username):
    salesman = Salesman.get_from_username(username)
    if salesman is None:
        raise ValueError(ErrorCode.customer_not_exist, ErrorMessage.customer_not_exist)
    else:
        return salesman


def check_request_params(*args):
    for i in args:
        if not i:
            raise ValueError(ErrorCode.params_lose, ErrorMessage.params_lose)


def get_customer_info(customer_id):
    try:
        if not customer_id:
            raise ValueError(ErrorCode.params_error, ErrorMessage.params_error)

        page = page_str_to_int()
        is_basic = request.args.get('is_basic', 'false')

        # 查看redis中是否存在客户信息
        ret = redis_store.get('customer_info_%s' % customer_id)
        if ret and (is_basic == "true"):
            current_app.logger.info('从redis中获取到客户信息')
            return ret.decode()

        # mysql中查询
        customer = get_customer_from_id(customer_id)
        customer_data = customer.to_basic_dict()

        # 序列化数据,转成json格式,存入缓存中
        json_customer = json.dumps(customer_data)
        redis_store.setex('customer_info_%s' % customer_id, constants.CUSTOMER_DETAIL_REDIS_EXPIRE_SECOND, json_customer)

        if is_basic == "true":
            return customer_data
        else:
            customer_data = customer.to_dict()

        # 追加客户小记分页
        customer_records = CustomerRecord.records_all(customer_id)

        customer_records_page, customer_records_list, total_page = paging(
            customer_records, page, constants.CUSTOMER_LIST_PAGE_CAPACITY)

        customer_records_dict_list = [i.to_dict() for i in customer_records_list]

        data = {'customers': customer_data, 'customer_records_list': customer_records_dict_list,
                'total_page': total_page, 'current_page': page}
        return str(data)
    except Exception as e:
        current_app.logger.info(e)
        raise e


def get_customer_basic_list(salesman_id):
    try:
        page = page_str_to_int()

        # 所有客户
        if salesman_id == 0:
            customers = Customer.get_all()
        # 根据销售id查询对应客户
        else:
            if get_salesman_from_id(salesman_id):
                customers = Customer.get_one_all(salesman_id)
            else:
                raise ValueError(ErrorCode.salesman_not_exist, ErrorMessage.salesman_not_exist)

        customers_page, customer_list, total_page = paging(
            customers, page, constants.CUSTOMER_LIST_PAGE_CAPACITY)

        customer_dict_list = [i.to_basic_dict() for i in customer_list]

        data = {'customers': customer_dict_list, 'total_page': total_page, 'current_page': page}
        return str(data)
    except Exception as e:
        current_app.logger.info(e)
        raise e


def customer_data_save():
    try:
        customer_data = get_request_data()

        name = customer_data.get('name')
        telephone = customer_data.get('telephone')
        detail = customer_data.get('detail')
        # salesman_id = g.salesman_id
        salesman_id = 1

        check_request_params(name, telephone, detail, salesman_id)
        get_customer_obj_by_telephone(telephone)

        customer = Customer(name=name, telephone=telephone, detail=detail, salesman_id=salesman_id)
        Customer.add(customer)
        return True
    except Exception as e:
        current_app.logger.info(e)
        raise e


def customer_data_update(customer_id):
    try:
        customer_data = get_request_data()

        name = customer_data.get('name')
        telephone = customer_data.get('telephone')

        check_request_params(name, telephone)
        get_customer_obj_by_telephone(telephone)

        customer = get_customer_from_id(customer_id)
        customer.name = name
        customer.telephone = telephone
        customer.update()
        return True
    except Exception as e:
        current_app.logger.info(e)
        raise e


def customer_record_save(customer_id):
    try:
        customer_record_data = get_request_data()

        content = customer_record_data.get('content')
        # salesman_id = g.salesman_id
        salesman_id = 1

        check_request_params(content)

        customer_record = CustomerRecord(content=content, customer_id=customer_id, salesman_id=salesman_id)
        CustomerRecord.add(customer_record)
        return True
    except Exception as e:
        current_app.logger.info(e)
        raise e


def check_token(username, password, *args):
    try:
        salesman = get_salesman_from_username(username)

        if salesman.check_password(password):
            login_time = int(time.time())
            salesman.login_time = login_time
            salesman.update()
            token = Auth.encode_auth_token(Auth, salesman.id, login_time)
        if token:
            return token.decode()
        else:
            raise ValueError(ErrorCode.login_error, ErrorMessage.login_error)
    except Exception as e:
        current_app.logger.info(e)
        raise e


def login_data_save():
    try:
        salesman_data = get_request_data()

        username = salesman_data.get('username')
        password = salesman_data.get('password')

        check_request_params(username, password)
        return check_token(username, password)
    except Exception as e:
        current_app.logger.info(e)
        raise e


def salesman_register():
    try:
        salesman_data = get_request_data()

        username = salesman_data.get('username')
        password = salesman_data.get('password')
        name = salesman_data.get('name')
        job_code = salesman_data.get('job_code')

        check_request_params(username, password, name, job_code)
        salesman = get_salesman_from_username(username)

        if salesman:
            raise ValueError(ErrorCode.username_exist, ErrorMessage.username_exist)

        salesman = Salesman(username=username, name=name, job_code=job_code)
        salesman.set_password = password

        Salesman.add(salesman)
        return True
    except Exception as e:
        current_app.logger.info(e)
        raise e
