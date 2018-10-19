
from flask import Blueprint, render_template, request, redirect, url_for

from home.models import db

home_buleprint = Blueprint('home', __name__)


@home_buleprint.route('/create_db/')
def create_db():
    db.create_all()
    return '创建成功'


@home_buleprint.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')


@home_buleprint.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')


@home_buleprint.route('/index/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')


@home_buleprint.route('/auth/', methods=['GET', 'POST'])
def auth():
    if request.method == 'GET':
        return render_template('auth.html')


@home_buleprint.route('/booking/', methods=['GET', 'POST'])
def booking():
    if request.method == 'GET':
        return render_template('booking.html')


@home_buleprint.route('/detail/', methods=['GET', 'POST'])
def detail():
    if request.method == 'GET':
        return render_template('detail.html')


@home_buleprint.route('/lorders/', methods=['GET', 'POST'])
def lorders():
    if request.method == 'GET':
        return render_template('lorders.html')


@home_buleprint.route('/my/', methods=['GET', 'POST'])
def my():
    if request.method == 'GET':
        return render_template('my.html')


@home_buleprint.route('/myhouse/', methods=['GET', 'POST'])
def myhouse():
    if request.method == 'GET':
        return render_template('myhouse.html')


@home_buleprint.route('/newhouse/', methods=['GET', 'POST'])
def newhouse():
    if request.method == 'GET':
        return render_template('newhouse.html')


@home_buleprint.route('/orders/', methods=['GET', 'POST'])
def orders():
    if request.method == 'GET':
        return render_template('orders.html')


@home_buleprint.route('/profile/', methods=['GET', 'POST'])
def profile():
    if request.method == 'GET':
        return render_template('profile.html')


@home_buleprint.route('/search/', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('search.html')