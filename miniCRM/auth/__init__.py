from miniCRM.models import Salesman


def salesman_by_username(username):
    salesman = Salesman.query.filter_by(username=username).first()
    return salesman


def authentucate(username, password):
    salesman = salesman_by_username(username)
    if salesman and salesman.check_password(password):
        return salesman




