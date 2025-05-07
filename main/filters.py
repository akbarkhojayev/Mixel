from django_filters import rest_framework as filters
from .models import *


class BrandFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Brand
        fields = ['name']

class ProductFilter(filters.FilterSet):
    brand = filters.NumberFilter(field_name='product__brand_id')

    class Meta:
        model = Product
        fields = ['name', 'brand']