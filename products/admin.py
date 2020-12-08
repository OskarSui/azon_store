from django.contrib import admin
from .models import Category, Product, Review
from authentication.models import User

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Review)
