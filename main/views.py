from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, SAFE_METHODS
from .serializers import *
from django.shortcuts import get_object_or_404
from .pagination import CustomPageNumberPagination

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username', 'email']
    ordering_fields = ['date_joined']

class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class BrandListAPIView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['name']

class BrandCreateAPIView(generics.CreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdmin]

class BrandDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdmin]

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['created_at', 'price']

class CategoryCreateAPIView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin]

class CategoryRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin]


class SubCategoryListAPIView(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['created_at']

class SubCategoryCreateAPIView(generics.CreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [IsAdmin]

class SubCategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [IsAdmin]

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'brand__name']
    ordering_fields = ['created_at', 'price']

class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save()


class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAdmin()]
        return [IsAuthenticated()]

    def perform_update(self, serializer):
        product = self.get_object()
        if product.user != self.request.user:
            raise PermissionDenied(detail="You are not the owner of this product")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied(detail="You are not the owner of this product")
        instance.delete()

class ImageListAPIView(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['product__name']
    ordering_fields = ['main', 'product__name']

class ImageCreateAPIView(generics.CreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAdmin]

class ImageDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAdmin]

    def perform_update(self, serializer):
        image = self.get_object()
        if image.product.user != self.request.user:
            raise PermissionDenied("Bu mahsulotga oid rasm sizga tegishli emas.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.product.user != self.request.user:
            raise PermissionDenied("Bu mahsulotga oid rasmni o‘chirishga ruxsatingiz yo‘q.")
        instance.delete()

class CartItemListAPIView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['product__name']
    ordering_fields = ['created_at']

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

class CartItemCreateAPIView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CartItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        cart_item = self.get_object()
        if cart_item.user != self.request.user:
            raise PermissionDenied("Siz faqat o'z cart item'laringizni tahrirlay olasiz.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("Siz faqat o'z cart item'laringizni o'chirishingiz mumkin.")
        instance.delete()

class OrderListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    serializer_class = OrderSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name', 'phone_number']
    ordering_fields = ['created_at']

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).all()


class OrderCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        order = self.get_object()
        if order.user != self.request.user:
            raise PermissionDenied(detail="You are not the owner of this order.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied(detail="You are not the owner of this order.")
        instance.delete()

class OrderItemListAPIView(generics.ListAPIView):
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name', 'phone_number']
    ordering_fields = ['created_at']

    def get_queryset(self):
        return OrderItem.objects.filter(order__user=self.request.user).all()

    def get(self, request, *args, **kwargs):
        orders = self.get_queryset()
        serializer = OrderItemSerializer(orders, many=True)
        return Response(serializer.data)


class OrderItemCreateAPIView(generics.CreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class OrderItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return OrderItem.objects.none()
        return OrderItem.objects.filter(order__user=self.request.user)

    def perform_update(self, serializer):
        order_item = self.get_object()
        if order_item.order.user != self.request.user:
            raise PermissionDenied(detail="Siz bu order itemning egasi emassiz.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.order.user != self.request.user:
            raise PermissionDenied(detail="Siz bu order itemning egasi emassiz.")
        instance.delete()


class LikedItemListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['product__name']
    ordering_fields = ['created_at']

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
            return Response({"detail": "Product added to liked list."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Product is already in your liked list."}, status=status.HTTP_200_OK)

class LikedItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = LikedItem.objects.all()
    serializer_class = LikedItemSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return LikedItem.objects.none()
        return LikedItem.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        liked_item = self.get_object()
        if liked_item.user != self.request.user:
            raise PermissionDenied(detail="Siz bu liked itemning egasi emassiz.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied(detail="Siz bu liked itemning egasi emassiz.")
        instance.delete()



class VersusItemListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['product__name']
    ordering_fields = ['created_at']

    def get(self, request, *args, **kwargs):
        versus_items = VersusItem.objects.filter(user=request.user)
        serializer = VersusItemSerializer(versus_items, many=True)
        return Response(serializer.data)


class VersusItemCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = VersusItem.objects.all()
    serializer_class = VersusItemSerializer

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        if not product_id:
            return Response({"detail": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        versus_item, created = VersusItem.objects.get_or_create(user=request.user, product=product)

        if created:
            return Response({"detail": "Product added to Versus list."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Product is already in your Versus list."}, status=status.HTTP_200_OK)


class VersusItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = VersusItem.objects.all()
    serializer_class = VersusItemSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return VersusItem.objects.none()
        return VersusItem.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        versus_item = self.get_object()
        if versus_item.user != self.request.user:
            raise PermissionDenied(detail="Siz bu Versus itemning egasi emassiz.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied(detail="Siz bu Versus itemning egasi emassiz.")
        instance.delete()


class DiscountListAPIView(APIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['product__name']
    ordering_fields = ['created_at']

    def get(self, request, *args, **kwargs):
        discounts = Discount.objects.all()
        serializer = DiscountSerializer(discounts, many=True)
        return Response(serializer.data)

class DiscountCreateAPIView(generics.CreateAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [IsAdmin]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DiscountDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin]
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Discount.objects.none()
        return Discount.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        discount = self.get_object()
        if discount.user != self.request.user:
            raise PermissionDenied(detail="Siz bu discountni yangilash huquqiga ega emassiz.")
        serializer.save()

    def perform_destroy(self, instance):

        if instance.user != self.request.user:
            raise PermissionDenied(detail="Siz bu discountni o'chirish huquqiga ega emassiz.")
        instance.delete()

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
    permission_classes = [IsAdmin]

    def create(self, request, *args, **kwargs):
        product_pk = kwargs.get('product_pk')

        product = get_object_or_404(Product, pk=product_pk)

        if product.user != request.user:
            raise PermissionDenied("Siz bu mahsulot uchun rasm qo'shish huquqiga ega emassiz.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product)

        return Response(serializer.data, status=status.HTTP_201_CREATED)