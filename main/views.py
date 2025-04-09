from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from django.shortcuts import get_object_or_404
from .pagination import CustomPageNumberPagination

class UserListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username', 'email']
    ordering_fields = ['data_joined']

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class BrandListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['name']


    def get(self, request, *args, **kwargs):
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)

class BrandCreateAPIView(generics.CreateAPIView):
    queryset = Brand.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = BrandSerializer

class BrandDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def get_queryset(self):
        return Brand.objects.all()


class CategoryListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter , OrderingFilter]
    search_fields = ['name',]
    ordering_fields = ['created_at', 'price']

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class CategoryDetailAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()


class CategoryCreateAPIView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class SubCategoryListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name',]
    ordering_fields = ['created_at',]

    def get(self, request, *args, **kwargs):
        subcategories = SubCategory.objects.all()
        serializer = SubCategorySerializer(subcategories, many=True)
        return Response(serializer.data)

class SubCategoryCreateAPIView(generics.CreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [IsAuthenticated]

class SubCategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        return SubCategory.objects.all()


class ProductListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name','brand']
    ordering_fields = ['created_at', 'price']

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ImageListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

class ImageCreateAPIView(generics.CreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

class ImageDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ImageSerializer
    queryset = Image.objects.all()


class CartItemListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name',]
    ordering_fields = ['created_at',]

    def get(self, request, *args, **kwargs):
        cart_items = CartItem.objects.all()
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

class CartItemCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class CartItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return CartItem.objects.none()
        return CartItem.objects.filter(user=self.request.user)


class OrderListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['first_name','last_name','phone_number']
    ordering_fields = ['created_at',]

    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class OrderCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Order.objects.none()
        return Order.objects.filter(user=self.request.user)


class OrderItemListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        order_items = OrderItem.objects.all()
        serializer = OrderItemSerializer(order_items, many=True)
        return Response(serializer.data)

class OrderItemCreateAPIView(generics.CreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

class OrderItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return OrderItem.objects.none()
        return OrderItem.objects.filter(user=self.request.user)


class LikedItemListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['product__name',]
    ordering_fields = ['created_at',]

    def get(self, request, *args, **kwargs):
        liked_items = LikedItem.objects.filter(user=request.user)
        serializer = LikedItemSerializer(liked_items, many=True)
        return Response(serializer.data)

class ProductAddLikedApiView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikedItemSerializer
    def post(self, request, *args, **kwargs):

        product_id = request.data.get('product')
        if not product_id:
            return Response({"detail": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        liked_item, created = LikedItem.objects.get_or_create(user=request.user, product=product)
        if created:
            return Response({"detail": "Product added to liked list."},status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Product is already in your liked list."},status=status.HTTP_200_OK)

class LikedItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = LikedItem.objects.all()
    serializer_class = LikedItemSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return LikedItem.objects.none()
        return LikedItem.objects.filter(user=self.request.user)


class VersusItemListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['product__name',]
    ordering_fields = ['created_at',]

    def get(self, request, *args, **kwargs):
        versus_items = VersusItem.objects.all()
        serializer = VersusItemSerializer(versus_items, many=True)
        return Response(serializer.data)

class VersusItemCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = VersusItem.objects.all()
    serializer_class = VersusItemSerializer

class VersusItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = VersusItem.objects.all()
    serializer_class = VersusItemSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return VersusItem.objects.none()
        return VersusItem.objects.filter(user=self.request.user)

class DiscountListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['product__name',]
    ordering_fields = ['created_at',]

    def get(self, request, *args, **kwargs):
        discounts = Discount.objects.all()
        serializer = DiscountSerializer(discounts, many=True)
        return Response(serializer.data)

class DiscountCreateAPIView(generics.CreateAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [IsAuthenticated]

class DiscountDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Discount.objects.none()
        return Discount.objects.filter(user=self.request.user)


class MessageListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get(self, request, *args, **kwargs):
        messages = Message.objects.filter(user=request.user)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

class MessageCreateAPIView(generics.CreateAPIView):
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer


class MessageDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Message.objects.none()
        return Message.objects.filter(user=self.request.user)


class ProductImageCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Image.objects.filter(product__user=self.request.user)


    def create(self, request, *args, **kwargs):
        product_pk = kwargs.get('product_pk')
        product = get_object_or_404(Product, pk=product_pk)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product)

        return Response(serializer.data, status=status.HTTP_201_CREATED)