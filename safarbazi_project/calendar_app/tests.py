from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Product, Availability

class APITestCase(TestCase):
    def setup_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token SafarBazi')

    def setUp(self):
       
        # Create some test products and availability
        self.product = Product.objects.create(
            name='Test Product For Search',
            standard_capacity=1,
            adult_price=5000,
            child_price=4000,
            infant_price=3000,
        )
        self.availability = Availability.objects.create(
            product=self.product,
            date='2023-05-05',
            price=10000,
            available=True,
        )
        self.availability = Availability.objects.create(
            product=self.product,
            date='2023-05-06',
            price=10000,
            available=True,
        )

        # Create an API client with the static token
        self.client = APIClient()
        # self.setup_token()

    def test_product_list(self):
        # Test listing products
        self.setup_token()
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_create_product(self):
        # Test creating a product
        data = {
            "name": "New Product",
            "standard_capacity": 5,
            "adult_price": 1000,
            "child_price": 2000,
            "infant_price": 0
        }
        self.setup_token()
        response = self.client.post('/api/products/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_availability_list(self):
        # Test listing availability
        self.setup_token()
        response = self.client.get('/api/availabilities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_availability(self):
        # Test creating an availability
        data = {
            "product": self.product.id,
            "date": '1402-10-01',
            "price": 20000,
            "available": True
        }
        self.setup_token()
        response = self.client.post('/api/availabilities/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_search_view(self):
        # Test the search view
        data = {
            "start_date": '1402-02-15',
            "end_date": '1402-02-16',
            "adult_count": 2,
            "child_count": 1,
            "infant_count": 0
        }


        self.setup_token()
        response = self.client.post('/api/search/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Check that one product is returned in the search result

    def test_token_authentication(self):
        # Test Token Authentication
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Should return Unauthorized

        # Authenticate with the token
        self.setup_token()
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_token_authentication(self):
        # Test Token Authentication with an invalid token
        self.client.credentials(HTTP_AUTHORIZATION='Token InvalidToken')
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Should return Unauthorized
