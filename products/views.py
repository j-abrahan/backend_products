from django.contrib.auth.models import User
from rest_framework import generics
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer, UserSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.http import Http404
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

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
                    'to complete your purchase. Sorry, we will restock soon')
        else:
            product.quantity -= int(quantity)
            product.save()

        serializer.save(
            name=name,
            quantity=quantity,
            created_by=created_by)
            #product_id=self.kwargs['product_id'])

#class OrderList(APIView):
#
#    def get(self, request, format=None):
#        orders = Order.objects.all()
#        serializer = OrderSerializer(orders, many=True)
#        return Response(serializer.data)
#
#    def post(self, request, format=None):
#        serializer = OrderSerializer(name=self.request.data["name"],
#                                     quantity=self.request.data["quantity"],
#                                     created_by=self.request.user)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

