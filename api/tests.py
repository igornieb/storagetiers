from django.urls import resolve
from rest_framework.test import APITestCase
from api.views import *
from api.urls import TokenObtainPairView, TokenRefreshView
from core.models import *
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from api.serializers import PictureSerializer
from django.core.files.uploadedfile import SimpleUploadedFile


class UrlsTest(APITestCase):

    # Tests if all api urls are resolved correctly
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
        img = SimpleUploadedFile(name='test_image.png', content=open("media/test_image.png", 'rb').read(),
                                 content_type='image/png')
        data = {
            'name': "test",
            'img': img
        }
        response = self.client.post(self.url, data, format="multipart")
        serializer = PictureAddSerializer(Picture.objects.get(name='test'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_method_post_authenticated_invalid(self):
        data = {
            'name': "test",
            'img': "test_image.png"
        }
        response = self.client.post(self.url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(False, Picture.objects.filter(name="test").exists())


class TimePictureListTest(APITestCase):
    # tests TimePictureList view

    url = reverse('shared-picture-list')

    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.picture = Picture.objects.create(owner=Account.objects.get(user=self.user), img="imgmock.png")
        TimePicture.objects.create(picture=self.picture, time=400)

    def test_method_get_authorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        query = TimePicture.objects.filter(picture__owner=Account.objects.get(user=self.user))
        serializer = TimePictureSerializer(query, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_method_get_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.url)
        data = {
            "detail": "Authentication credentials were not provided."
            }
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, data)


class PictureDetailsTests(APITestCase):

    def setUp(self):
        user = User.objects.create_user(username='admin', password='admin')
        self.account = Account.objects.get(user=user)
        self.account.tier = Tier.objects.get(name="Enterprise")
        self.account.save()
        self.picture = Picture.objects.create(owner=self.account, img="image.jpg")
        self.picture.img = SimpleUploadedFile(name='test_image.jpg', content=open("media/test_image.png", 'rb').read(),
                                              content_type='image/jpeg')
        self.picture.save()
        self.uuid = self.picture.id
        self.token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('picture-details', kwargs={'pk': self.uuid})
        self.url_height = reverse('picture-details', kwargs={'pk': self.uuid, 'height': 400})

    def test_method_post_authenticated_valid(self):
        # tests creating timelinks (valid_data)
        data = {
            'time': 800
        }
        response = self.client.post(self.url, data, format='json')
        object = TimePicture.objects.filter(time=800).first()
        serializer = TimePictureShortSerializer(object)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_method_post_authenticated_invalid(self):
        # tests creating timelinks (invalid data)
        data = {
            'time': 1
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(False, TimePicture.objects.filter(time=1).exists())

    def test_method_post_unauthenticated(self):
        # tests creating timelinks (unauthorized)
        self.client.force_authenticate(user=None, token=None)
        data = {
            'time': 800
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(False, TimePicture.objects.filter(time=800).exists())

    def test_method_get(self):
        # test get method
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_method_get_fake_uuid(self):
        # test get method with uuid that doesnt exists
        response = self.client.get(reverse('picture-details', kwargs={'pk': '76807036-29ff-4f3a-a336-42bf2168ab27'}))
        response_height = self.client.get(reverse('picture-details', kwargs={'pk': '76807036-29ff-4f3a-a336-42bf2168ab27', 'height':400}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_height.status_code, status.HTTP_404_NOT_FOUND)

    def test_method_get_height(self):
        # test get method with height
        response = self.client.get(self.url_height)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TimePictureDetailsTest(APITestCase):
    # tests TimePictureDetails view
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        picture = Picture.objects.create(owner=Account.objects.get(user=self.user), img="imgmock.png")
        picture.img = SimpleUploadedFile(name='test_image.jpg', content=open("media/test_image.png", 'rb').read(),
                                         content_type='image/jpeg')
        picture.save()
        self.picture_good = TimePicture.objects.create(picture=picture, time=400)
        self.picture_bad = TimePicture.objects.create(picture=picture, time=0)

    def test_method_get_active(self):
        response = self.client.get(reverse('timelink', kwargs={'pk': self.picture_good.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_method_get_expired(self):
        response = self.client.get(reverse('timelink', kwargs={'pk': self.picture_bad.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
