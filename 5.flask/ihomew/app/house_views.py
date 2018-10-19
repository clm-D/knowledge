import os
from operator import and_

from flask import Blueprint, render_template, session, jsonify, request

from app.models import User, House, Area, Facility, HouseImage, db, Order
from utils import status_code
from utils.functions import is_login
from utils.settings import UPLOAD_DIR

house_blueprint = Blueprint('house', __name__)


@house_blueprint.route('/myhouse/', methods=['GET'])
@is_login
def myhouse():
    return render_template('myhouse.html')


@house_blueprint.route('/myhouse_get/', methods=['GET'])
@is_login
def myhouse_get():
    user = User.query.get(session['user_id'])
    if not (user.id_card and user.id_name):
        return jsonify(status_code.HOUSE_USER_INFO_ID_CARD_INVALID)
    houses = House.query.filter(House.user_id == session['user_id']).order_by('-id')
    houses_list = [house.to_dict() for house in houses]
    return jsonify({'code': status_code.OK, 'houses_list': houses_list})


@house_blueprint.route('/newhouse/', methods=['GET'])
@is_login
def newhouse():
    return render_template('newhouse.html')


@house_blueprint.route('/house_info_get/', methods=['GET'])
def house_info_get():
    areas = Area.query.all()
    facilitys = Facility.query.all()

    area_list = [area.to_dict() for area in areas]
    facility_list = [facility.to_dict() for facility in facilitys]

    return jsonify({'code': '200', 'area_list': area_list, 'facility_list': facility_list})


@house_blueprint.route('/newhouse_post/', methods=['POST'])
@is_login
def newhouse_post():
    house = House()
    house.user_id = session['user_id']
    house.title = request.form.get('title')
    house.price = request.form.get('price')
    house.area_id = request.form.get('area_id')
    house.address = request.form.get('address')
    house.room_count = request.form.get('room_count')
    house.acreage = request.form.get('acreage')
    house.unit = request.form.get('unit')
    house.capacity = request.form.get('capacity')
    house.beds = request.form.get('beds')
    house.deposit = request.form.get('deposit')
    house.min_days = request.form.get('min_days')
    house.max_days = request.form.get('max_days')

    facilitys = request.form.getlist('facility')
    for facility_id in facilitys:
        facility = Facility.query.get(facility_id)
        house.facilities.append(facility)
    house.add_update()

    return jsonify({'code': status_code.OK, 'house_id': house.id})


@house_blueprint.route('/house_image_post/', methods=['POST'])
@is_login
def house_image_post():
    image = request.files.get('house_image')
    house_id = request.form.get('house_id')
    file_path = os.path.join(UPLOAD_DIR, image.filename)
    image.save(file_path)
    # 保存到数据库中
    house_image = HouseImage()
    house_image.house_id = house_id
    image_url = os.path.join('upload', image.filename)
    house_image.url = image_url
    house_image.add_update()
    # 创建房屋首图
    house = House.query.get(house_id)
    if not house.index_image_url:
        house.index_image_url = image_url
        house.add_update()
    return jsonify({'code': '200', 'image_url': image_url})


@house_blueprint.route('/detail/', methods=['GET'])
@is_login
def detail():
    return render_template('detail.html')


@house_blueprint.route('/detail_get/<int:id>/', methods=['GET'])
def detail_get(id):
    house = House.query.get(id)
    house_list = house.to_full_dict()
    return jsonify(code=status_code.OK, house_list=house_list)


@house_blueprint.route('/index/', methods=['GET'])
def index():
    return render_template('index.html')


@house_blueprint.route('/index_get/', methods=['GET'])
def index_get():
    user_id = session['user_id']
    if user_id:
        user = User.query.get(user_id)
        username = user.name
    else:
        username = ''

    houses = House.query.all()
    houses_list = [house.to_dict() for house in houses]
    areas = Area.query.all()
    area_list = [area.to_dict() for area in areas]

    return jsonify(code=status_code.OK, username=username, houses_list= houses_list, area_list=area_list)


@house_blueprint.route('/search/', methods=['GET'])
def search():
    return render_template('search.html')


@house_blueprint.route('/search_get/', methods=['GET'])
def search_get():
    aid = request.args.get('aid')
    sd = request.args.get('sd')
    ed = request.args.get('ed')
    sk = request.args.get('sk')

    # 过滤地区信息
    houses = House.query.filter(House.area_id == aid)
    # 过滤自己发布的房源
    if session['user_id']:
        houses_list = houses.filter(House.user_id != session['user_id'])

    # 查找出不满足时间条件的房屋id
    order1 = Order.query.filter(Order.begin_date <= sd, Order.end_date >= ed)
    order2 = Order.query.filter(Order.begin_date <= sd, sd < Order.end_date, Order.end_date <= ed)
    order3 = Order.query.filter(sd <= Order.begin_date, Order.begin_date < ed, ed <= Order.end_date)
    order4 = Order.query.filter(sd <= Order.begin_date, Order.end_date <= ed)
    houses_id1 = [order.house_id for order in order1]
    houses_id2 = [order.house_id for order in order2]
    houses_id3 = [order.house_id for order in order3]
    houses_id4 = [order.house_id for order in order4]

    houses_ids = list(set(houses_id1 + houses_id2 + houses_id3 + houses_id4))

    # 过滤掉不满足时间条件的房源
    houses_list1 = houses_list.filter(House.id.notin_(houses_ids))

    if sk == 'booking':
        houses_list1 = houses_list1.order_by('order_count')
    elif sk == 'price-inc':
        houses_list1 = houses_list1.order_by('price')
    elif sk == 'price-des':
        houses_list1 = houses_list1.order_by('-price')
    else:
        houses_list1 = houses_list1.order_by('id')
    houses_dict = [house.to_dict() for house in houses_list1]

    return jsonify(code=status_code.OK, houses_dict=houses_dict)