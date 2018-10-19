from functools import wraps

from flask import redirect, url_for, session


def is_login(func):
    @wraps(func)
    def check(*args, **kwargs):
        try:
            flog = session['login_status']
        except:
            return redirect(url_for('app.login'))
        return func(*args, **kwargs)
    return check