from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Model


class User(AbstractUser):

    isadmin = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    card_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    icon = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.name

class Galary(models.Model):
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = "Galaries"


class Brand(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    details = models.TextField()
    is_cash = models.BooleanField(default=True)
    price = models.FloatField()
    monthly_price = models.FloatField()
    country = models.CharField(max_length=100)
    discount = models.FloatField(blank=True, null=True)
    discount_price = models.FloatField(blank=True, null=True)
    discount_date_finished = models.DateField(blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    galary = models.ForeignKey(Galary, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Image(models.Model):
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    main = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name


class PropertyType(models.Model):
    title = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Property(models.Model):
    title = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.title} : {self.value}"

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Order(models.Model):
    STATUS_CHOICES = (
        ('Toplanyapti', 'Toplanyapti'),
        ('Yetib keldi', 'Yetib keldi'),
        ('Yetkazilmoqda', 'Yetkazilmoqda'),
        ('Topshirildi', 'Topshirildi'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.FloatField()
    phone_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    payment_type = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default='Toplanyapti')

    def __str__(self):
        return self.user.username

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.amount * self.product.price

    def __str__(self):
        return self.product.name

class LikedItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name

class VersusItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE , blank=True, null=True)

    def __str__(self):
        return self.product.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    file = models.FileField(upload_to='files/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

