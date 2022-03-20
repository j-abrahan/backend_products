from .models import Product, Order
from rest_framework import serializers

class OrderSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Order
        fields = ('name', 'quantity', 'created_by')

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'quantity')
