from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^products/$', views.ProductList.as_view(), name='product-list'),
]
