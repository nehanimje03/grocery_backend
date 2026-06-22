from django.urls import path
from products.APIs.product import *


urlpatterns = [
    path('all-products/', AllProductsAPIView.as_view()),
    path('popular-products/', PopularProductsAPIView.as_view()),

]