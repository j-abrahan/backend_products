from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^products/$',
            views.ProductList.as_view(),
            name='product-list'
    ),
    re_path(r'^products/(?P<product_id>[0-9]+)/$',
            views.ProductDetail.as_view(),
            name='product-detail'
    ),
    re_path(r'^products/orders/$',
            views.OrderList.as_view(),
            name='order-list'
    ),
]
