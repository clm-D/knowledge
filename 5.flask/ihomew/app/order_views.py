
import datetime

from flask import Blueprint, render_template, request, session, jsonify

from app.models import House, Order
from utils import status_code

order_blueprint = Blueprint('order', __name__)


@order_blueprint.route('/booking/', methods=['GET'])
def booking():
    return render_template('booking.html')


@order_blueprint.route('/orders_post/', methods=['POST'])
def orders_post():
    house_id = request.form.get('house_id')
    start_date = request.form.get('start_date')
    start_time = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = request.form.get('end_date')
    end_time = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    days = (end_time-start_time).days + 1
    price = House.query.get(house_id).price
    amount = days * price

    order = Order()
    order.user_id = session['user_id']
    order.house_id = request.form.get('house_id')
    order.begin_date = start_time
    order.end_date = end_time
    order.days = days
    order.house_price = price
    order.amount = amount
    order.add_update()

    return jsonify(status_code.OK)


@order_blueprint.route('/booking_post/', methods=['POST'])
def booking_post():
    house_id = request.form.get('house_id')
    house = House.query.get(house_id)
    if session['user_id'] == house.user_id:
        return jsonify(status_code.ORDER_HOUSE_USER_ID_IS_SESSION_ID)

    start_date = request.form.get('start_date')
    start_time = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = request.form.get('end_date')
    end_time = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    days = (end_time-start_time).days + 1
    price = House.query.get(house_id).price
    amount = days * price

    order = Order()
    order.user_id = session['user_id']
    order.house_id = request.form.get('house_id')
    order.begin_date = start_time
    order.end_date = end_time
    order.days = days
    order.house_price = price
    order.amount = amount
    order.add_update()

    return jsonify(code=status_code.OK)


@order_blueprint.route('/orders/', methods=['GET'])
def orders():
    return render_template('orders.html')


@order_blueprint.route('/orders_get/', methods=['GET'])
def orders_get():
    orders_all = Order.query.filter(Order.user_id == session['user_id'])
    orders_list = [order.to_dict() for order in orders_all]
    return jsonify(code=status_code.OK, orders_list=orders_list)


@order_blueprint.route('/lorders/', methods=['GET'])
def lorders():
    return render_template('lorders.html')


@order_blueprint.route('/lorders_get/', methods=['GET'])
def lorders_get():
    houses = House.query.filter(House.user_id == session['user_id'])
    house_list = [house.id for house in houses]
    orders_all = Order.query.filter(Order.house_id.in_(house_list))
    orders_list = [order.to_dict() for order in orders_all]
    return jsonify(code=status_code.OK, orders_list=orders_list)


@order_blueprint.route('/lorders_patch/', methods=['PATCH'])
def lorders_patch():
    order_id = request.form.get('order_id')
    status = request.form.get('status')
    comment = request.form.get('comment')

    order = Order.query.get(order_id)
    order.status = status
    if comment:
        order.comment = comment
    order.add_update()
    return jsonify(status_code.SUCCESS)