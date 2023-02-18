from django.db import models
from core.utilis import validate_sizes_allowed


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
