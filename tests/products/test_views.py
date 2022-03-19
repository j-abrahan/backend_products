import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from products.models import Product

UserModel = get_user_model()

NUMBER_OF_PRODUCTS_IN_INITIAL_MIGRATION = 6

class APITestCaseAdmin(APITestCase):
    @pytest.mark.django_db
    def setUp(self):
        self.user = UserModel.objects.create_superuser(
            username='admin', email='', password='root')
        token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

class TestProductList(APITestCase):
    @pytest.mark.django_db
    def test_get_product_list(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), NUMBER_OF_PRODUCTS_IN_INITIAL_MIGRATION)

class TestProductListAdmin(APITestCaseAdmin):
    @pytest.mark.django_db
    def test_admin_can_post_new_product(self):
        url = reverse('product-list')

        new_product = {
                "name": "Aquarius",
                "price": "1.50",
                "quantity": 10
        }

        response = self.client.post(url, new_product, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), NUMBER_OF_PRODUCTS_IN_INITIAL_MIGRATION + 1)

    @pytest.mark.django_db
    def test_non_admin_cannot_post_new_product(self):
        url = reverse('product-list')

        new_product = {
                "name": "Aquarius",
                "price": "1.50",
                "quantity": 10
        }

        self.client.logout()
        response = self.client.post(url, new_product, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Product.objects.count(), NUMBER_OF_PRODUCTS_IN_INITIAL_MIGRATION)
