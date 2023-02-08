from functools import wraps
from flask import g, redirect, url_for


# 登录装饰器
def login_request(func):
    # 保留func的信息
    @wraps(func)
    def inner(*args, **kwargs):
        if g.user:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('user.login'))
    return inner