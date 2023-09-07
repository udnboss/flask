import functools
from flask import abort
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from sqlalchemy.inspection import inspect

class DictConverter(object):

    def as_dict(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def as_dict_list(l):
        return [m.serialize() for m in l]
     
def require_permission(permission):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.has_permission(permission):
                # print(current_user.permissions, permission)
                abort(403)  # HTTP 403 Forbidden
            return func(*args, **kwargs)
        return wrapper
    return decorator