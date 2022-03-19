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

class TestProductListNonAdmin(APITestCase):
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

class TestProductDetailNonAdmin(APITestCase):
    @pytest.mark.django_db
    def test_can_get_product_detail(self):
        url = reverse('product-detail', kwargs={'product_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestProductDetailAdmin(APITestCaseAdmin):
    @pytest.mark.django_db
    def test_admin_can_delete_a_product(self):
        url = reverse('product-detail', kwargs={'product_id': 1})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), NUMBER_OF_PRODUCTS_IN_INITIAL_MIGRATION - 1)

    @pytest.mark.django_db
    def test_non_admin_cannot_delete_a_product(self):
        url = reverse('product-detail', kwargs={'product_id': 1})

        # Logout so the user is non admin
        self.client.logout()

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Product.objects.count(), NUMBER_OF_PRODUCTS_IN_INITIAL_MIGRATION)

    @pytest.mark.django_db
    def test_admin_can_update_a_product(self):
        url = reverse('product-detail', kwargs={'product_id': 1})

        new_product = {
                "name": "Coca-cola",
                "price": "2.00",
                "quantity": 8
        }

        response = self.client.put(url, new_product, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), NUMBER_OF_PRODUCTS_IN_INITIAL_MIGRATION)
        self.assertEqual(response.json()['price'], '2.00')
        self.assertEqual(response.json()['quantity'], 8)

    @pytest.mark.django_db
    def test_admin_can_patch_a_product(self):
        url = reverse('product-detail', kwargs={'product_id': 1})

        new_product = {
                "price": "2.00",
        }

        response = self.client.patch(url, new_product, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), NUMBER_OF_PRODUCTS_IN_INITIAL_MIGRATION)
        self.assertEqual(response.json()['price'], '2.00')
