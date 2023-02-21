import uuid
from django.utils import timezone
from datetime import timedelta, datetime
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from core.utilis import validate_sizes_allowed, validate_time_allowed
from storagetiers.settings import MEDIA_ROOT


class Tier(models.Model):
    def __str__(self):
        return self.name

    def get_sizes(self):
        # returns list of allowed heights
        val_list = self.sizes_allowed.split(" ")
        res = []
        for val in val_list:
            if val.isdigit():
                res.append(int(val))
        res.sort()
        return res

    name = models.CharField(max_length=100, unique=True)
    sizes_allowed = models.CharField(max_length=100, validators=[validate_sizes_allowed])
    allow_original = models.BooleanField(default=False)
    allow_link = models.BooleanField(default=False)


class Account(models.Model):
    # this model extends built-in User model adding tier column\

    def __str__(self):
        return f"{self.user.username} - {self.tier}"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE)


class Picture(models.Model):
    # this model stores user uploaded pictures
    def __str__(self):
        return f"{self.name} - {self.owner}"

    def upload_to(self, filename):
        return f"media/{self.owner.user}/{filename}"

    def get_absolute_url(self):
        # get posible res, create dicts
        heights = self.get_sizes()
        links = []
        for value in heights:
            if isinstance(value, int):
                links.append(reverse("picture-details", kwargs={'pk': self.pk, "height": value}))
            if value == "":
                links.append(reverse("picture-details", kwargs={'pk': self.pk}))
        return links

    def get_sizes(self):
        # returns list of allowed heights
        val_list = str(self.owner.tier.sizes_allowed).split(" ")
        res = []
        for val in val_list:
            if val.isdigit():
                res.append(int(val))
        res.sort()
        if self.owner.tier.allow_original:
            res.append('')
        if self.owner.tier.allow_link:
            res.append('linkable')
        return res

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    img = models.ImageField(upload_to=upload_to, null=False, blank=False, validators=[FileExtensionValidator((['jpg', 'png']))])


class TimePicture(models.Model):
    def __str__(self):
        return f"{self.picture} {self.created} {self.expires}"

    def get_absolute_url(self):
        return reverse("timelink", kwargs={'pk': self.pk})

    def is_expired(self):
        if self.expires > timezone.now():
            return False
        else:
            self.expired = True
            self.save()
            return True

    def time_left(self):
        time_left = (self.expires - timezone.now()).total_seconds()
        if time_left < 0:
            self.expired = True
            self.save()
            return "Expired"
        return time_left

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    time = models.IntegerField(null=False, validators=[validate_time_allowed])
    expires = models.DateTimeField(default=timezone.now, null=True)
    expired = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.expires = self.created + timedelta(seconds=self.time)
        super(TimePicture, self).save(*args, **kwargs)

