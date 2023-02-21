from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta, datetime
from core.models import Account, User, Tier, Picture, TimePicture


class AccountModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # creates testuser User
        User.objects.create(username='testuser')

    def test_if_account_exist(self):
        # tests if accoutnt was created by signal
        account = Account.objects.filter(user=User.objects.get(username='testuser')).exists()
        self.assertEqual(True, account)

    def test_str_representation(self):
        # tests string representation of Model
        account = Account.objects.get(user=User.objects.get(username='testuser'))
        expected_object_name = f'{account.user.username} - {account.tier}'
        self.assertEqual(str(account), expected_object_name)


class TierModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # creates test tier
        Tier.objects.create(name="TestTier", sizes_allowed="200 300 800")

    def test_if_default_tiers_exists(self):
        # test if default tiers exists
        tiers = Tier.objects.filter(name="Basic").exists() and Tier.objects.filter(
            name="Premium").exists() and Tier.objects.filter(name="Enterprise").exists()
        self.assertEqual(True, tiers)

    def test_str_representation(self):
        # tests string representation of Model
        tier = Tier.objects.get(name="TestTier")
        expected_object_name = f'{tier.name}'
        self.assertEqual(str(tier), expected_object_name)

    def test_allowed_sizes(self):
        tier = Tier.objects.get(name="TestTier")
        expected_sizes_allowed = [200, 300, 800]
        self.assertEqual(tier.get_sizes(), expected_sizes_allowed)

    def test_validation_sizes_allowed_error(self):
        invalid_sizes = ["200;800", "200, 800", "300i"]
        with self.assertRaises(ValidationError):
            for sizes in invalid_sizes:
                tier = Tier(name="test", sizes_allowed=sizes)
                tier.full_clean()

    def test_validation_sizes_allowed(self):
        valid_sizes = ["200 800", "200 800 1000", "300"]
        for sizes in valid_sizes:
            tier = Tier(name="test", sizes_allowed=sizes)
            tier.full_clean()


class PictureModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        t = Tier.objects.create(name="TestTier", sizes_allowed="200 300")
        u = User.objects.create(username='testuser')
        a = Account.objects.get(user=u)
        a.tier = t
        a.save()
        Picture.objects.create(name="TestPicture", img="", owner=a)

    def test_str_representation(self):
        picture = Picture.objects.filter(name="TestPicture").first()
        expected_object_name = f'{picture.name} - {picture.owner}'
        self.assertEqual(str(picture), expected_object_name)

    def test_get_absolute_url(self):
        picture = Picture.objects.filter(name="TestPicture").first()
        expected_urls = [
            reverse("picture-details", kwargs={'pk': picture.pk, "height": 200}),
            reverse("picture-details", kwargs={'pk': picture.pk, "height": 300})
        ]
        self.assertEqual(picture.get_absolute_url(), expected_urls)

    def test_allowed_sizes(self):
        picture = Picture.objects.filter(name="TestPicture").first()
        expected_sizes_allowed = [200, 300]
        self.assertEqual(picture.get_sizes(), expected_sizes_allowed)


class TimePictureModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        u = User.objects.create(username='testuser')
        a = Account.objects.get(user=u)
        cls.picture = Picture.objects.create(name="TestPicture", img="", owner=a)
        TimePicture.objects.create(picture=cls.picture, time=400)

    def test_validation_time_field_error(self):
        invalid_times = [399, 30001, 20]
        with self.assertRaises(ValidationError):
            for time in invalid_times:
                picture1 = TimePicture(picture=self.picture, time=time)
                picture1.full_clean()

    def test_validation_time_field(self):
        valid_times = [400, 3000, 300]
        for time in valid_times:
            picture1 = TimePicture(picture=self.picture, time=time)
            picture1.full_clean()

    def test_str_representation(self):
        picture = TimePicture.objects.filter(picture=self.picture).first()
        expected_object_name = f'{picture.picture} {picture.created} {picture.expires}'
        self.assertEqual(str(picture), expected_object_name)

    def test_get_absolute_url(self):
        picture = TimePicture.objects.filter(picture=self.picture).first()
        expected_urls = reverse("timelink", kwargs={'pk': picture.pk})
        self.assertEqual(picture.get_absolute_url(), expected_urls)

    def test_is_expired(self):
        picture = TimePicture.objects.filter(picture=self.picture).first()
        expected_bool = picture.created + timedelta(seconds=picture.time) > timezone.now()
        self.assertEqual(picture.is_expired(), not expected_bool)

    def test_expires_field(self):
        picture = TimePicture.objects.filter(picture=self.picture).first()
        expected_expires = picture.created + timedelta(seconds=picture.time)
        self.assertEqual(picture.expires, expected_expires)
