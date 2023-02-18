from rest_framework import serializers
from core.models import Picture


class PictureSerializer(serializers.ModelSerializer):
    # TODO get_absolute_url
    class Meta:
        model = Picture
        fields = ['owner', 'img']
