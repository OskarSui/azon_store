from django.contrib import admin
from django.urls import path, include
# from .serializers import UserSerializer
from .views import (ProductList,
                    ProductListAPIVIew,
                    CategoryViewSet,
                    SellerViewSet
                   )
from rest_framework.routers import DefaultRouter


category_list = CategoryViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

category_detail = CategoryViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

router = DefaultRouter(trailing_slash=False)
router.register('categories', CategoryViewSet)
router.register('sellers', SellerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('products/', ProductList.as_view()),
    path('products-filter/', ProductListAPIVIew.as_view()),
    # path('add-products/', ReportView.as_view()),
    path('categories/', category_list, name='category-list'),
    path('categories/<int:pk>/', category_detail, name='category-detail'),
]