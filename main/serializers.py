from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "password", "image", "phone_number", "card_number", "date_joined"]
        extra_kwargs = {
            "password": {"write_only": True},
            "date_joined": {"read_only": True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = '__all__'


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'user', 'product', 'product_name', 'product_price', 'amount', 'total_price', 'created_at']
        read_only_fields = ['user', 'created_at']

    def get_total_price(self, obj):
        return obj.amount * obj.product.price


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'product_name', 'product_price', 'amount', 'total_price', 'created_at']
        read_only_fields = ['created_at']

    def get_total_price(self, obj):
        return obj.amount * obj.product.price


class LikedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikedItem
        fields = '__all__'


class VersusItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = VersusItem
        fields = '__all__'


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

