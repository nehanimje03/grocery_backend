from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductListSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    discount_percentage = serializers.SerializerMethodField()
    product_images = serializers.SerializerMethodField()
    stock_status = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id","name","price","description","category","subcategory",
            "sizes","stock","stock_status","is_popular",
            "discount_percentage","product_images","created_by"
        ]

    def get_price(self, obj):
        price = obj.price
        return int(price) if price == int(price) else float(price)

    def get_discount_percentage(self, obj):
        if obj.discount_percentage:
            return f"{int(obj.discount_percentage)}%"
        return "0%"

    def get_stock_status(self, obj):
        if obj.stock <= 0:
            return "out_of_stock"
        return "in_stock"

    def get_product_images(self, obj):
        request = self.context.get("request")
        images = obj.product_image.all()

        if request:
            return [
                request.build_absolute_uri(img.image.url)
                for img in images
            ]
        return [img.image.url for img in images]
    


class CartItemSerializer(serializers.ModelSerializer):
    product_details = ProductListSerializer(source='product', read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id','product','product_details','quantity','size','color','subtotal']

    def get_subtotal(self, obj):
        return float(obj.product.price * obj.quantity)


