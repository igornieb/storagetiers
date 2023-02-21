from django.urls import resolve
from rest_framework.test import APITestCase
from api.views import *
from api.urls import TokenObtainPairView, TokenRefreshView
from core.models import *
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from api.serializers import PictureSerializer


class UrlsTest(APITestCase):

    # Tests if all urls are resolved correctly
    def test_pictures_url(self):
        url = reverse('picture-list')
        self.assertEqual(resolve(url).func.view_class, PictureList)

    def test_pictures_shared_url(self):
        url = reverse('shared-picture-list')
        self.assertEqual(resolve(url).func.view_class, TimePictureList)

    def test_token_url(self):
        url = reverse('token-obtain-pair')
        self.assertEqual(resolve(url).func.view_class, TokenObtainPairView)

    def test_token_refresh_url(self):
        url = reverse('token-refresh')
        self.assertEqual(resolve(url).func.view_class, TokenRefreshView)

    def test_picture_details(self):
        url = reverse('picture-details', kwargs={'pk': "3574baa7-e238-484e-8691-8d1c2287e06e"})
        url_height = reverse('picture-details', kwargs={'pk': "3574baa7-e238-484e-8691-8d1c2287e06e", 'height': 200})
        self.assertEqual(resolve(url).func.view_class, PictureDetails)
        self.assertEqual(resolve(url_height).func.view_class, PictureDetails)

    def test_timepicture_details(self):
        url = reverse('timelink', kwargs={'pk': "3574baa7-e238-484e-8691-8d1c2287e06e"})
        self.assertEqual(resolve(url).func.view_class, TimePictureDetails)


class PictureListTests(APITestCase):
    # tests PictureList view

    url = reverse('picture-list')

    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_method_get_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_method_get_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_method_post_authenticated_valid(self):
        data = {
            'name': "test",
            'img': "nice_image.jpg"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "test")


class TimePictureListTest(APITestCase):
    # tests TimePictureList view

    url = reverse('shared-picture-list')

    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        picture = Picture.objects.create(owner=Account.objects.get(user=self.user), img="imgmock.png")
        TimePicture.objects.create(picture=picture, time=400)

    def test_method_get_authorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_method_get_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PictureDetailsTests(APITestCase):

    def setUp(self):
        user = User.objects.create_user(username='admin', password='admin')
        a = Account.objects.get(user=user)
        a.tier = Tier.objects.get(name="Enterprise")
        a.save()
        self.picture = Picture.objects.create(owner=a, img="image.jpg")
        self.uuid = self.picture.id
        self.token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('picture-details', kwargs={'pk': self.uuid})
        self.url_height = reverse('picture-details', kwargs={'pk': self.uuid, 'height': 200})

    def test_method_post_authenticated_valid(self):
        data = {
            'time': 800
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['time'], 800)
        self.assertEqual(response.data["picture"], PictureSerializer(self.picture).data)

    def test_method_post_authenticated_invalid(self):
        data = {
            'time': 1
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_method_post_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        data = {
            'time': 800
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

