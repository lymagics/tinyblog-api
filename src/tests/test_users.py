from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class CommonData:
    """
    Common data for user tests.
    """

    SETUP_DATA = {
        'username': 'bob',
        'email': 'bob@example.com',
        'password': 'cat',
    }

    STATUS_CREATED = status.HTTP_201_CREATED
    STATUS_SUCCESS = status.HTTP_200_OK
    STATUS_FAILED = status.HTTP_400_BAD_REQUEST


class TestUserAPI(CommonData, APITestCase):
    """
    User API test case.
    """

    VALID_DATA = {
        'username': 'alice',
        'email': 'alice@example.com',
        'password': 'dog',
    }

    INVALID_DATA = {
        'username': 'bob',
        'email': 'bob@example.com',
    }

    INVALID_DATA_MESSAGES = {
        'username': ['A user with that username already exists.'],
        'email': ['user with this email already exists.'],
        'password': ['This field is required.'],
    }

    URL = reverse('api:users:users-list')

    def setUp(self):
        self.user = User.objects.create_user(**self.SETUP_DATA)
        self.URL_DETAIL = reverse('api:users:users-detail', kwargs={'username': self.user.username})

    def test_creating_user(self):
        """
        Test user creation flow with valid data.
        """
        response = self.client.post(self.URL, self.VALID_DATA)
        self.assertEqual(response.status_code, self.STATUS_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_not_creating_user(self):
        """
        Test user creation flow with invalid data.
        """
        response = self.client.post(self.URL, self.INVALID_DATA)
        self.assertEqual(response.status_code, self.STATUS_FAILED)

        errors = response.json()
        self.assertEqual(errors, self.INVALID_DATA_MESSAGES)

    def test_retrieving_user(self):
        """
        Test user retrieving flow.
        """
        response = self.client.get(self.URL_DETAIL)
        self.assertEqual(response.status_code, self.STATUS_SUCCESS)

        data = response.json()
        self.assertEqual(data['username'], self.user.username)
        self.assertEqual(data['avatar_url'], self.user.avatar_url)
        self.assertEqual(data['about_me'], self.user.about_me)

    def test_retrieving_list_users(self):
        """
        Test user list retrieving flow.
        """
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, self.STATUS_SUCCESS)

        data = response.json()
        self.assertTrue('results' in data)
        self.assertTrue('count' in data)
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['count'], 1)


class TestMeAPI(CommonData, APITestCase):
    """
    Current user API test case.
    """

    UPDATE_DATA = {
        'username': 'alice',
        'email': 'alice@example.com',
        'about_me': 'Python Developer.',
    }

    URL = reverse('api:users:me')
    STATUS_UNAUTHORIZED = status.HTTP_401_UNAUTHORIZED

    def setUp(self):
        self.user = User.objects.create_user(**self.SETUP_DATA)

    def test_retrieving_user(self):
        """
        Test current user retrieving flow.
        """
        self._provide_authentication()

        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, self.STATUS_SUCCESS)

        data = response.json()
        self.assertEqual(data['username'], self.user.username)
        self.assertEqual(data['avatar_url'], self.user.avatar_url)
        self.assertEqual(data['about_me'], self.user.about_me)

    def test_retrieving_user_without_credentials(self):
        """
        Test current user retrieving without credentials flow.
        """
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, self.STATUS_UNAUTHORIZED)

    def test_updating_user(self):
        """
        Test current user updating flow.
        """
        self._provide_authentication()
        response = self.client.put(self.URL, self.UPDATE_DATA)
        self.assertEqual(response.status_code, self.STATUS_SUCCESS)

        self.user.refresh_from_db()
        data = response.json()
        self.assertEqual(data['username'], self.user.username)
        self.assertEqual(data['avatar_url'], self.user.avatar_url)
        self.assertEqual(data['about_me'], self.user.about_me)

    def _provide_authentication(self):
        """
        Provide token authentication for test requests.
        """
        token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')
