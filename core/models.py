from django.contrib.auth.models import User
from django.db import models
from core.utilis import validate_sizes_allowed
from storagetiers.settings import MEDIA_ROOT


class Tier(models.Model):
    def __str__(self):
        return self.name

    def get_sizes(self):
        # returns list of allowed heights
        val_list = str(self.sizes_allowed).split(" ")
        res = []
        for val in val_list:
            if val.isdigit():
                res.append(int(val))
        return res

    name = models.CharField(max_length=100)
    sizes_allowed = models.CharField(max_length=100, validators=[validate_sizes_allowed])
    store_original = models.BooleanField(default=False)
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
        return f"{self.pk} - {self.owner}"

    def upload_to(self, filename):
        return f"{MEDIA_ROOT}/{self.owner.user}/{filename}"

    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    img = models.ImageField(upload_to=upload_to,)
