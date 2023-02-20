from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from posts.models import Post
from users.models import User


class TestPostAPI(APITestCase):
    """
    Post API test case.
    """

    USER_DATA = {
        'username': 'bob',
        'email': 'bob@example.com',
        'password': 'cat',
    }

    INITIAL_POST_DATA = {
        'text': 'Hello, World!'
    }

    VALID_DATA = {
        'text': 'First post!',
    }

    INVALID_DATA_MESSAGES = {
        'text': ['This field is required.'],
    }

    UPDATE_DATA = {
        'text': 'Goodbye, World!',
    }

    URL = reverse('api:posts:posts-list')
    STATUS_CREATED = status.HTTP_201_CREATED
    STATUS_SUCCESS = status.HTTP_200_OK
    STATUS_FAILED = status.HTTP_400_BAD_REQUEST
    STATUS_DELETED = status.HTTP_204_NO_CONTENT

    def setUp(self):
        self.user = User.objects.create_user(**self.USER_DATA)
        self.post = Post.objects.create(author=self.user, **self.INITIAL_POST_DATA)
        self.URL_DETAIL = reverse('api:posts:posts-detail', kwargs={'pk': self.post.pk})

    def test_creating_post(self):
        """
        Test post creating flow.
        """
        self._provide_authentication()

        response = self.client.post(self.URL, self.VALID_DATA)
        self.assertEqual(response.status_code, self.STATUS_CREATED)

    def test_not_creating_post(self):
        """
        Test post not creating flow.
        """
        self._provide_authentication()

        response = self.client.post(self.URL, {})
        self.assertEqual(response.status_code, self.STATUS_FAILED)

        errors = response.json()
        self.assertEqual(errors, self.INVALID_DATA_MESSAGES)

    def test_retrieving_post(self):
        """
        Test post retrieving flow.
        """
        response = self.client.get(self.URL_DETAIL)
        self.assertEqual(response.status_code, self.STATUS_SUCCESS)

        data = response.json()
        self.assertEqual(data['text'], self.post.text)
        self.assertEqual(data['author']['username'], self.post.author.username)

    def test_retrieving_list_post(self):
        """
        Test post list retrieving flow.
        """
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, self.STATUS_SUCCESS)

        data = response.json()
        self.assertTrue('count' in data)
        self.assertTrue('results' in data)
        self.assertEqual(data['count'], Post.objects.count())
        self.assertEqual(len(data['results']), Post.objects.count())

    def test_updating_post(self):
        """
        Test post updating flow.
        """
        self._provide_authentication()

        response = self.client.put(self.URL_DETAIL, self.UPDATE_DATA)
        self.assertEqual(response.status_code, self.STATUS_SUCCESS)

        self.post.refresh_from_db()
        data = response.json()
        self.assertEqual(data['text'], self.post.text)

    def test_deleting_post(self):
        """
        Test post deleting flow.
        """
        self._provide_authentication()

        response = self.client.delete(self.URL_DETAIL)
        self.assertEqual(response.status_code, self.STATUS_DELETED)

    def test_retrieving_specific_user_list_post(self):
        """
        Test specific user post list retrieving flow.
        """
        url = reverse('api:users:users-posts', kwargs={'username': self.user.username})

        response = self.client.get(url)
        self.assertEqual(response.status_code, self.STATUS_SUCCESS)

        data = response.json()
        self.assertTrue('count' in data)
        self.assertTrue('results' in data)
        self.assertEqual(data['count'], self.user.posts.count())
        self.assertEqual(len(data['results']), self.user.posts.count())

    def _provide_authentication(self):
        """
        Provide token authentication for test requests.
        """
        token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')
