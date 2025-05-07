from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Category, Galary, Brand, Product, Image,
    PropertyType, Property, CartItem, Order, OrderItem,
    LikedItem, VersusItem, Message
)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'isadmin', 'phone_number', 'card_number', 'is_staff')
    search_fields = ('username', 'email', 'phone_number')
    list_filter = ('isadmin', 'is_staff')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Qo‘shimcha maʼlumotlar', {
            'fields': ('image', 'phone_number', 'card_number', 'isadmin'),
        }),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Galary)
class GalaryAdmin(admin.ModelAdmin):
    list_display = ('id',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

class PropertyTypeInline(admin.TabularInline):
    model = PropertyType
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'monthly_price', 'is_cash', 'discount', 'brand', 'category')
    list_filter = ('is_cash', 'brand', 'category')
    search_fields = ('name',)
    inlines = [ImageInline, PropertyTypeInline]

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'main')
    list_filter = ('main',)
    search_fields = ('product__name',)

class PropertyInline(admin.TabularInline):
    model = Property
    extra = 1

@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'product')
    inlines = [PropertyInline]

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'property_type')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'product__name')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'phone_number', 'region', 'city')
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'amount', 'total_price', 'created_at')
    search_fields = ('order__user__username', 'product__name')

@admin.register(LikedItem)
class LikedItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')

@admin.register(VersusItem)
class VersusItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'category')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at')
    search_fields = ('user__username', 'message')
