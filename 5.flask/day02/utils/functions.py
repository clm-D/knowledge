from functools import wraps

from flask import session, redirect, url_for


def is_login(func):
    @wraps(func)
    def check(*args, **kwargs):
        try:
            login_status = session['login_status']
        except:
            return redirect(url_for('app.login'))
        return func(*args, **kwargs)
    return check