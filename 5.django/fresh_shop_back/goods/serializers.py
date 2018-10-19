
from rest_framework import serializers

from goods.models import Goods


class GoodsSerializer(serializers.ModelSerializer):

    class Meta:
        # 指定学历化的模型
        model = Goods
        # 指定序列化哪些字段
        fields = ['id', 'category', 'name', 'goods_sn',
                  'click_nums', 'sold_nums', 'fav_nums',
                  'goods_nums', 'market_price', 'shop_price',
                  'goods_brief', 'goods_desc', 'ship_free',
                  'goods_front_image', 'is_new', 'is_hot', 'add_time']