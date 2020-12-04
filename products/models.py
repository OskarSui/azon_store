from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser

class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Seller(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

# class User(AbstractUser):
#     instagram_handle = models.CharField(max_length=255, default="", blank=True)

class Product(models.Model):
    photo = models.URLField(max_length=500)
    asin = models.CharField(unique=True, max_length=100)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products')
    price = models.FloatField(validators=[MinValueValidator(0)])
    title = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    updated = models.DateTimeField(auto_now_add=True)
    available_inventory = models.PositiveIntegerField(default=0)
#
# class Cart(models.Model):
#     """A model that contains data for a shopping cart."""
#     customer = models.OneToOneField(
#         # settings.AUTH_USER_MODEL,
#         related_name='cart'
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
# class CartItem(models.Model):
#     """A model that contains data for an item in the shopping cart."""
#     cart = models.ForeignKey(
#         Cart,
#         related_name='items',
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True
#     )
#     product = models.ForeignKey(
#         Product,
#         related_name='items',
#         on_delete=models.CASCADE
#     )
#     quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
#
#     def __unicode__(self):
#         return '%s: %s' % (self.product.title, self.quantity)
#
# class Order(models.Model):
#     """
#     An Order is the more permanent counterpart of the shopping cart. It represents
#     the frozen the state of the cart on the moment of a purchase. In other words,
#     an order is a customer purchase.
#     """
#     customer = models.ForeignKey(
#         # settings.AUTH_USER_MODEL,
#         related_name='orders',
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True
#     )
#     total = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
# class OrderItem(models.Model):
#     """A model that contains data for an item in an order."""
#     order = models.ForeignKey(
#         Order,
#         related_name='order_items',
#         on_delete=models.CASCADE
#     )
#     product = models.ForeignKey(
#         Product,
#         related_name='order_items',
#         on_delete=models.CASCADE
#     )
#     quantity = models.PositiveIntegerField(null=True, blank=True)
#
#     def __unicode__(self):
#         return '%s: %s' % (self.product.title, self.quantity)