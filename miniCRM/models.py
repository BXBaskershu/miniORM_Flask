from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class Salesman(db.Model):
    """销售人员"""

    __tablename__ = "salesmen"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True, nullable=False)  # 用户名
    password = db.Column(db.String(128), nullable=False)  # 加密的密码
    name = db.Column(db.String(20))  # 真实姓名
    job_code = db.Column(db.String(30), index=True)  # 工号
    is_incumbency = db.Column(db.SMALLINT, default=1)  # 是否在职, 默认1在职， 0不在职
    created_time = db.Column(db.DateTime, default=datetime.now)

    # 通过装饰器property，把password方法提升为属性
    @property
    def password(self):
        raise AttributeError("不可读")

    @password.setter
    def password(self, passwd):
        """密码加密"""
        self.password = generate_password_hash(passwd)

    def check_password(self, passwd):
        """检查密码"""
        return check_password_hash(self.password_hash, passwd)

    def to_dict(self):
        """将对象转换为字典数据"""
        salesman_dict = {
            "username": self.username,
            "name": self.name,
            "job_code": self.job_code,
            "created_time": self.created_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return salesman_dict


class Customer(db.Model):
    """客户"""

    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, nullable=False)
    telephone = db.Column(db.String(20), unique=True, index=True, nullable=False)
    salesman_id = db.Column(db.Integer, db.ForeignKey('salesmen.id'), index=True, nullable=False)
    detail = db.Column(db.String(200), nullable=False)
    created_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        """将对象转换为字典数据"""
        customer_dict = {
            "name": self.name,
            "telephone": self.telephone,
            "salesman_id": self.salesman_id,
            "detail": self.detail,
        }
        return customer_dict

    def to_basic_dict(self):
        """只转化基本信息"""
        customer_dict = {
            "name": self.name,
            "telephone": self.telephone
        }
        return customer_dict


class CustomerRecord(db.Model):
    """客户跟进记录"""

    __tablename__ = "customer_records"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), index=True, nullable=False)
    salesman_id = db.Column(db.Integer, db.ForeignKey('salesmen.id'), index=True, nullable=False)
    content = db.Column(db.String(200), nullable=False)  # 跟进记录
    created_time = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        """将对象转换为字典数据"""
        customer_record_dict = {
            "content": self.content,
            "salesman_id": self.salesman_id,
            "created_time": self.created_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return customer_record_dict