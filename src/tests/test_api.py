from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from parameterized import parameterized


class TestRequest(APITestCase):
    """
    Common API features test case.
    """

    URLS = {
        'users': reverse('api:users:users-list'),
        'posts': reverse('api:posts:posts-list'),
    }

    @parameterized.expand([
        (URLS['users'],
         status.HTTP_200_OK),
        (URLS['posts'],
         status.HTTP_200_OK)
    ])
    def test_response_codes(self, endpoint, expected_status_code):
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, expected_status_code)
