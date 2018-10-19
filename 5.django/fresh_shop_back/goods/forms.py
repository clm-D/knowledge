
from django import forms

from goods.models import GoodsCategory


class GoodsForm(forms.Form):

    name = forms.CharField(required=True, error_messages={'required': '商品名必填'})
    goods_sn = forms.CharField(required=True, error_messages={'required': '商品货号必填'})
    category = forms.CharField(required=True, error_messages={'required': '分类必填'})
    goods_nums = forms.CharField(required=True, error_messages={'required': '商品库存必填'})
    market_price = forms.CharField(required=True, error_messages={'required': '商品市场价必填'})
    shop_price = forms.CharField(required=True, error_messages={'required': '商品本店价必填'})
    goods_brief = forms.CharField(required=True, error_messages={'required': '商品描述必填'})
    goods_front_image = forms.ImageField(required=False)

    def clean_category(self):
        # 验证字段，返回category对象
        category_id = self.cleaned_data['category']
        # 获取分类对象
        category = GoodsCategory.objects.filter(category_type=category_id).first()
        if category:
            return category
        else:
            raise forms.ValidationError({'category': '商品分类选择有误'})