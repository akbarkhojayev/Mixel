from rest_framework import serializers
from rest_framework.response import Response

from .permissions import *

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password' ,'isadmin']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        user.isadmin = validated_data.get('isadmin', False)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "password", "image", "phone_number", "card_number", "date_joined", "isadmin"]
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
        fields = ['id', 'name', 'image', 'icon',]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class LikedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikedItem
        fields = ['user', 'product']
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['title', 'value', 'property_type']

    def create(self, validated_data):
        property_type_instance = validated_data.get('property_type')
        if not property_type_instance:
            raise serializers.ValidationError('PropertyType is required.')

        return super().create(validated_data)


class PropertyTypeSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()

    class Meta:
        model = PropertyType
        fields = ['id', 'title', 'value', 'product']

    def get_value(self, obj):
        properties = Property.objects.filter(property_type=obj)

        return [{'type': prop.title, 'value': prop.value} for prop in properties]

    def create(self, validated_data):
        product_instance = validated_data.get('product')
        if not product_instance:
            raise serializers.ValidationError('Product is required for PropertyType.')

        return super().create(validated_data)


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    main_image = serializers.SerializerMethodField()
    like = serializers.SerializerMethodField()
    like_id = serializers.SerializerMethodField()
    is_cart = serializers.SerializerMethodField()
    properties = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    versus = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'details', 'is_cash', 'price', 'monthly_price',
            'country', 'brand', 'category', 'category_name' ,'images', 'main_image',
            'like', 'like_id','is_cart','versus', 'discount','discount_price','discount_date_finished' ,'properties' , 'galary'

        ]

    def get_images(self, obj):
        images = obj.image_set.all()
        return ImageSerializer(images, many=True, context=self.context).data

    def get_main_image(self, obj):
        main_img = obj.image_set.filter(main=True).first()
        if main_img:
            return self.context['request'].build_absolute_uri(main_img.image.url)
        return None

    def get_like(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return LikedItem.objects.filter(user=user, product=obj).exists()
        return False

    def get_versus(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return VersusItem.objects.filter(user=user, product=obj).exists()
        return False

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return LikedItem.objects.filter(user=user, product=obj).values_list('id', flat=True).first()
        return False

    def get_category_name(self, obj):
        if obj.category:
                return obj.category.name
        return None

    def get_is_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return CartItem.objects.filter(user=user, product=obj).exists()
        return False

    def get_properties(self, obj):
        property_types = PropertyType.objects.filter(product=obj)
        return PropertyTypeSerializer(property_types, many=True).data

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')
    product_image = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'user', 'product', 'product_image', 'product_name', 'product_price', 'amount', 'total_price', 'created_at']
        read_only_fields = ['user', 'created_at']

    def get_product_image(self, obj):
        main_image = obj.product.image_set.filter(main=True).first()
        request = self.context.get('request')
        if main_image and request:
            return request.build_absolute_uri(main_image.image.url)
        return None

    def get_total_price(self, obj):
        return obj.amount * obj.product.price

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



class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['user', 'total_price', 'created_at', 'status']

class OrderCreateSerializer(serializers.ModelSerializer):
    cart_item_ids = serializers.ListField(
        child=serializers.IntegerField(), required=True, write_only=True
    )

    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    phone_number = serializers.CharField(max_length=20)
    address = serializers.CharField(max_length=255)
    payment_type = serializers.CharField(max_length=50)

    class Meta:
        model = Order
        fields = ['cart_item_ids', 'first_name', 'last_name', 'phone_number', 'address', 'payment_type']

    def create(self, validated_data):
        user = self.context['request'].user
        cart_item_ids = validated_data.get('cart_item_ids')

        cart_items = CartItem.objects.filter(id__in=cart_item_ids, user=user)


        if not cart_items.exists():
            raise serializers.ValidationError("Tanlangan CartItemlar topilmadi.")

        order = Order.objects.create(
            user=user,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
            address=validated_data['address'],
            payment_type=validated_data['payment_type'],
            total_price=0,
        )

        total = 0

        # Tanlangan CartItemlarni OrderItemga qo‘shish
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                amount=item.amount
            )
            total += item.amount * item.product.price  # Total narxini hisoblash

        # Orderning umumiy narxini yangilash
        order.total_price = total
        order.save()

        # Savatdagi tanlangan CartItemlarni o'chirish
        cart_items.delete()

        return order


# class VersusItemSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = VersusItem
#         fields = ['user' , 'product']
#         read_only_fields = ['user']
#
#     def create(self, validated_data):
#         validated_data['user'] = self.context['request'].user
#         return super().create(validated_data)

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class GalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Galary
        fields = '__all__'

class LikedItemListSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = LikedItem
        fields = ['id','user', 'product']
        read_only_fields = ['user']

class VersusItemSerializer(serializers.ModelSerializer):
    product_properties = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    product_price = serializers.SerializerMethodField()
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = VersusItem
        fields = ['id', 'product','product_name' , 'product_price' , 'product_image' , 'product_properties']

    def get_product_properties(self, obj):
        properties = Property.objects.filter(property_type__product=obj.product)
        return [{'type': p.title, 'value': p.value} for p in properties]

    def get_product_name(self, obj):
        return obj.product.name

    def get_product_price(self, obj):
        return obj.product.price

    def get_product_image(self, obj):
        image = obj.product.image_set.filter(main=True).first()
        if image and hasattr(image, 'image'):
            return image.image.url
        return None
