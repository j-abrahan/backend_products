from django.contrib.auth.models import User
from rest_framework import generics
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer, RegisterSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from django.http import Http404
from rest_framework import serializers

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminOrReadOnly, )
    lookup_url_kwarg = 'product_id'

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminOrReadOnly, )
    lookup_url_kwarg = 'product_id'

class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def list(self, request):
        queryset = Order.objects.filter(created_by=request.user.id)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        name = self.request.data["name"]
        quantity = self.request.data["quantity"]
        created_by = self.request.user
        product = Product.objects.filter(name=name).first()
        if product is None:
            raise Http404

        if product.quantity - int(quantity) < 0:
            raise serializers.ValidationError(
                    'We do not have enough inventory of ' + name  + \
                    ' to complete your purchase. The product will be in stock soon' )
        else:
            product.quantity -= int(quantity)
            product.save()

        serializer.save(
            name=name,
            quantity=quantity,
            created_by=created_by)
