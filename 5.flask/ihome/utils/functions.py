from functools import wraps

from flask import session, redirect, url_for


def is_login(func):
    @wraps(func)
    def check(*args, **kwargs):
        try:
            user_id = session['user_id']
        except:
            return redirect(url_for('user.login'))
        return func(*args, **kwargs)
    return check