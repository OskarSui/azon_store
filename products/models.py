from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser
from azon import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)

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
    # slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    updated = models.DateTimeField(auto_now_add=True)
    review = GenericRelation('review')
    # available_inventory = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.title


class Review(models.Model):
    """Отзывы"""
    # title = models.ForeignKey(max_length=250)
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True, related_name="children"
    )
    product = models.ForeignKey(Product, verbose_name="продукт", on_delete=models.CASCADE, related_name="review")

    def __str__(self):
        return f"{self.name} - {self.product}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return "Продукт: {} (для корзины)".format(self.content_object.title)
    #
    # def save(self, *args, **kwargs):
    #     self.final_price = self.qty * self.content_object.price
    #     super().save(*args, **kwargs)

    class Cart(models.Model):
        owner = models.ForeignKey('Customer', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
        products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
        total_products = models.PositiveIntegerField(default=0)
        final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая цена')
        in_order = models.BooleanField(default=False)
        for_anonymous_user = models.BooleanField(default=False)

        def __str__(self):
            return str(self.id)

    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey('content_type', 'object_id')



# class Cart(models.Model):
#     """A model that contains data for a shopping cart."""
#     customer = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.DO_NOTHING,
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
#         settings.AUTH_USER_MODEL,
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