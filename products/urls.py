from django.urls import path
from products.APIs.Cart.cart import *
from products.APIs.Product.product import *
from products.APIs.Product.products_filter import *
from products.APIs.Product.related_product_details import *


urlpatterns = [
    path('product-filter/',ProductFilterAPIView.as_view()),
    path('products-detail/', PublicProductDetailAPIView.as_view()),
    path('related-products/', PublicProductDetailAPIView.as_view()),
    path('all-products/', PublicProductsAPIView.as_view()),
    path('latest-products/', PublicProductsAPIView.as_view()),
    path('bestseller-products/', PublicProductsAPIView.as_view()),
    path('popular-products/', PublicProductsAPIView.as_view()),




    # cart 
    path('add-to-cart/', CartAPIView.as_view()),
    path('get-items-from-cart/',CartAPIView.as_view()),
    path('update-cart-item-details/',CartAPIView.as_view()),
    path('remove-items-from-cart/',CartAPIView.as_view()),
    path('increase-product-quantity/', CartAPIView.as_view()),
    path('decrease-product-quantity/', CartAPIView.as_view()),


]