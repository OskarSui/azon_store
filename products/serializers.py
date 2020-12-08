from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Category, Product, Seller, Review
from django.contrib.auth.models import User

class FilterReviewListSerializer(serializers.Serializer):
    """Вывод рекурсивно children"""
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Вывод рекурсивно children"""
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class CategorySerializer(ModelSerializer):
    random_photo = SerializerMethodField()

    def get_random_photo(self, obj):
        try:
            return obj.products.first().photo
        except:
            return ""

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'random_photo'
        )


class SellerSerializer(ModelSerializer):
    class Meta:
        model = Seller
        fields = (
            'id',
            'name'
        )


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'photo',
            'price',
            'title',
            'category',
            'seller',
            'photo',
        )


class ProductsAllInfoSerializer(ModelSerializer):
    category = CategorySerializer()
    seller = SellerSerializer()

    class Meta:
        model = Product
        fields = (
            'id',
            'photo',
            'price',
            'title',
            'category',
            'seller',
            'photo',
        )

class ReviewCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        # fields = '__all__'
        exclude = ['email']


class ReviewSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializers_class = FilterReviewListSerializer
        model = Review
        fields = ('name', 'title', 'text', 'children')



# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'instagram_handle')
#
# class CartSerializer(serializers.ModelSerializer):
#
#     """Serializer for the Cart model."""
#
#     customer = UserSerializer(read_only=True)
#     # used to represent the target of the relationship using its __unicode__ method
#     items = serializers.StringRelatedField(many=True)
#
#     class Meta:
#         model = Cart
#         fields = (
#             'id', 'customer', 'created_at', 'updated_at', 'items'
#         )
#
# class CartItemSerializer(serializers.ModelSerializer):
#
#     """Serializer for the CartItem model."""
#
#     cart = CartSerializer(read_only=True)
#     product = ProductSerializer(read_only=True)
#
#     class Meta:
#         model = CartItem
#         fields = (
#             'id', 'cart', 'product', 'quantity'
#         )
#
# class OrderSerializer(serializers.ModelSerializer):
#
#     """Serializer for the Order model."""
#
#     customer = UserSerializer(read_only=True)
#     # used to represent the target of the relationship using its __unicode__ method
#     order_items = serializers.StringRelatedField(many=True, required=False)
#
#     class Meta:
#         model = Order
#         fields = (
#             'id', 'customer', 'total', 'created_at', 'updated_at', 'order_items'
#         )
#
#     def create(self, validated_data):
#         """Override the creation of Order objects
#         Parameters
#         ----------
#         validated_data: dict
#         """
#         order = Order.objects.create(**validated_data)
#         return order
#
# class OrderItemSerializer(serializers.ModelSerializer):
#
#     """Serializer for the OrderItem model."""
#
#     order = OrderSerializer(read_only=True)
#     product = ProductSerializer(read_only=True)
#
#     class Meta:
#         model = OrderItem
#         fields = (
#             'id', 'order', 'product', 'quantity'
#         )
