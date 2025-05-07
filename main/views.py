from collections import defaultdict
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, SAFE_METHODS
from .serializers import *
from .pagination import CustomPageNumberPagination


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

class UserListAPIView(generics.ListAPIView):
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
    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter,]
    filterset_fields = ['category']
    search_fields = ['name']
    ordering_fields = ['name',]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='category',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Category id filter',
            ),
        ]
    )

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)



class BrandCreateAPIView(generics.CreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdmin]
    parser_classes = [MultiPartParser, FormParser]


class BrandDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdmin]


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend , SearchFilter, OrderingFilter]
    filterset_fields = ['name','brand']
    search_fields = ['name']
    ordering_fields = ['created_at', 'price']
    parser_classes = [MultiPartParser, FormParser]


class CategoryCreateAPIView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin]


class CategoryRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin]
class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['brand', 'category' ,'galary']
    search_fields = ['name', 'brand__name']
    ordering_fields = ['created_at', 'price']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='brand',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Brand id filter',
            ),
            openapi.Parameter(
                name='category',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Category id filter',
            ),
            openapi.Parameter(
                name='galary',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Galary id filter',

            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class FilterProductAPIView(APIView):
    def filter_products(self, products, filters):
        min_price = filters.get("minPrice")
        if min_price:
            try:
                products = products.filter(price__gte=float(min_price))
            except ValueError:
                pass

        max_price = filters.get("maxPrice")
        if max_price:
            try:
                products = products.filter(price__lte=float(max_price))
            except ValueError:
                pass

        categories = filters.get("category", [])
        if isinstance(categories, (str, int)):
            categories = [categories]
        if categories:
            if all(str(c).isdigit() for c in categories):
                products = products.filter(category__id__in=categories)
            else:
                products = products.filter(category__name__in=categories)

        brands = filters.get("brand", [])
        if isinstance(brands, (str, int)):
            brands = [brands]
        if brands:
            if all(str(b).isdigit() for b in brands):
                products = products.filter(brand__id__in=brands)
            else:
                products = products.filter(brand__name__in=brands)

        return products

    def post(self, request):
        products = Product.objects.all()
        filtered_products = self.filter_products(products, request.data)
        serializer = ProductSerializer(filtered_products, many=True, context={'request': request})
        return Response({"products": serializer.data}, status=status.HTTP_200_OK)



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

class GalaryListAPIView(generics.ListAPIView):
    queryset = Galary.objects.all()
    serializer_class = GalarySerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = CustomPageNumberPagination

class GalaryCreateAPIView(generics.CreateAPIView):
    queryset = Galary.objects.all()
    serializer_class = GalarySerializer
    permission_classes = [IsAdmin]
    parser_classes = [MultiPartParser, FormParser]

class GalaryRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = GalarySerializer
    permission_classes = [AllowAny]

    def get_object(self):
        queryset = Galary.objects.all()
        return get_object_or_404(queryset, pk=self.kwargs['pk'])

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
    parser_classes = [MultiPartParser, FormParser]


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
    serializer_class = OrderCreateSerializer

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
    serializer_class = OrderItemSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name', 'phone_number']
    ordering_fields = ['created_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return OrderItem.objects.filter(order__user=user)
        return OrderItem.objects.none()

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


class LikedItemListAPIView(generics.ListAPIView):
    queryset = LikedItem.objects.all()
    serializer_class = LikedItemListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['created_at', 'price']
    search_fields = ['product__name']

    def get_queryset(self):
        return LikedItem.objects.filter(user=self.request.user)

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


# class VersusItemCreateAPIView(generics.CreateAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = VersusItem.objects.all()
#     serializer_class = VersusItemSerializer
#
#     def post(self, request, *args, **kwargs):
#         product_id = request.data.get('product')
#         if not product_id:
#             return Response({"detail": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             product = Product.objects.get(id=product_id)
#         except Product.DoesNotExist:
#             return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
#
#         versus_item, created = VersusItem.objects.get_or_create(user=request.user, product=product)
#
#         if created:
#             return Response({"detail": "Product added to Versus list."}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({"detail": "Product is already in your Versus list."}, status=status.HTTP_200_OK)
#

# class VersusItemListAPIView(generics.ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = VersusItemSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['category']
#
#     def get_queryset(self):
#         return VersusItem.objects.filter(user=self.request.user)


class VersusItemListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        versus_items = VersusItem.objects.filter(user=user).select_related('product__category', 'product')
        serializer = VersusItemSerializer(versus_items, many=True)

        grouped_data = defaultdict(list)
        for item in serializer.data:
            category_name = VersusItem.objects.get(id=item['id']).product.category.name
            grouped_data[category_name].append(item)

        return Response(grouped_data)


class VersusItemCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VersusItemSerializer

    def perform_create(self, serializer):
        user = self.request.user
        product = serializer.validated_data['product']

        if VersusItem.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("Bu product allaqachon qo‘shilgan.")
        serializer.save(user=user, category=product.category)


class VersusItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VersusItemSerializer

    def get_queryset(self):
        return VersusItem.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        if self.get_object().user != self.request.user:
            raise PermissionDenied("Siz bu Versus itemning egasi emassiz.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("Siz bu Versus itemning egasi emassiz.")
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


class PropertyTypeListCreateView(generics.ListCreateAPIView):
    queryset = PropertyType.objects.all()
    serializer_class = PropertyTypeSerializer
    permission_classes = (AllowAny,)

class PropertyTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PropertyType.objects.all()
    serializer_class = PropertyTypeSerializer
    permission_classes = (AllowAny,)

class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = (AllowAny,)

class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = (AllowAny,)