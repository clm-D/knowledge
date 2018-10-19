import flask
from flask import request, abort, render_template, flash, redirect, url_for
from flask_login import login_user

import user
from login import app



@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not all([username, password]):
        login_user(user)

        flash('Logged in successfully.')

        next = flask.request.args.get('next')

        # if not is_safe_url(next):
        #     return flask.abort(400)

        return redirect(next or url_for('index'))
    return flask.render_template('login.html')