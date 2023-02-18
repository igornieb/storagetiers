from django.db import models
from core.utilis import validate_sizes_allowed


class Tier(models.Model):
    name = models.CharField(max_length=100)
    sizes_allowed = models.CharField(max_length=100, validators=[validate_sizes_allowed])
    store_original = models.BooleanField(default=False)
    allow_link = models.BooleanField(default=False)
