from django.contrib import admin
from django.urls import path
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.views import token_obtain_pair , token_refresh
from main.views import *
from django.conf import settings
from django.conf.urls.static import static
from main.models import *

schema_view = get_schema_view(
   openapi.Info(
      title="Market API",
      default_version='v1',
      description="Test",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('users/', UserListAPIView.as_view(), name='user-list-create'),
    path('users/me' , UserRetrieveUpdateDestroyAPIView.as_view(), name='user-retrieve-update'),
    path('users/register' , RegisterAPIView.as_view(), name='user-register'),
    path('brands/', BrandListAPIView.as_view(), name='brand-list-create'),
    path('brands/create', BrandCreateAPIView.as_view(),),
    path('brands/<int:pk>/', BrandDetailAPIView.as_view(), name='brand-detail'),
    path('categories/', CategoryListAPIView.as_view(), name='category-list-create'),
    path('categories/create', CategoryCreateAPIView.as_view(),),
    path('categories/<int:pk>/', CategoryRetrieveUpdateAPIView.as_view(), name='category-detail'),
    path('products/', ProductListAPIView.as_view(), name='product-list-create'),
    path('products/filter/' , FilterProductAPIView.as_view(), name='product-filter'),
    path('products/create/', ProductCreateAPIView.as_view() ),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-detail'),
    path('images/', ImageListAPIView.as_view(), name='image-list-create'),
    path('images/craete', ImageCreateAPIView.as_view()),
    path('images/<int:pk>/', ImageDetailAPIView.as_view(), name='image-detail'),
    path('cart-items/', CartItemListAPIView.as_view(), name='cartitem-list-create'),
    path('cart-items/create', CartItemCreateAPIView.as_view(), ),
    path('cart-items/<int:pk>/', CartItemDetailAPIView.as_view(), name='cartitem-detail'),
    path('orders/', OrderListAPIView.as_view(), name='order-list-create'),
    path('orders/create', OrderCreateAPIView.as_view(),),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
    path('order-items/', OrderItemListAPIView.as_view(), name='orderitem-list-create'),
    path('order-items/create/', OrderItemCreateAPIView.as_view(), ),
    path('order-items/<int:pk>/', OrderItemDetailAPIView.as_view(), name='orderitem-detail'),
    path('liked-items/', LikedItemListAPIView.as_view(), name='likeditem-list-create'),
    path('liked-items/add/' , ProductAddLikedApiView.as_view(), name='likeditem-add'),
    path('liked-items/<int:pk>/', LikedItemDetailAPIView.as_view(), name='likeditem-detail'),
    path('versus-items/', VersusItemListAPIView.as_view(), name='versusitem-list-create'),
    path('versus-items/add/', VersusItemCreateAPIView.as_view(),),
    path('versus-items/<int:pk>/', VersusItemDetailAPIView.as_view(), name='versusitem-detail'),
    path('messages/', MessageListAPIView.as_view(), name='message-list-create'),
    path('messages/create/', MessageCreateAPIView.as_view(), ),
    path('messages/<int:pk>/', MessageDetailAPIView.as_view(), name='message-detail'),
    path('property-types/', PropertyTypeListCreateView.as_view(), name='property-type-list-create'),
    path('property-types/<int:pk>/', PropertyTypeDetailView.as_view(), name='property-type-detail'),
    path('properties/', PropertyListCreateView.as_view(), name='property-list-create'),
    path('properties/<int:pk>/', PropertyDetailView.as_view(), name='property-detail'),
    path("galary/", GalaryListAPIView.as_view(),),
    path('galary/<int:pk>/', GalaryRetrieveAPIView.as_view(), name='galary-detail'),
    path("galary/create", GalaryCreateAPIView.as_view(),),
]

urlpatterns += [
    path('token/', token_obtain_pair ),
    path('token/refresh/', token_refresh ),
]