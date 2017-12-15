from functools import wraps
from flask import current_app
from miniCRM.exception import DBCommitException
from miniCRM import db


def commit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            raise DBCommitException

        return ret

    return wrapper
