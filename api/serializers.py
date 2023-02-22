from rest_framework import serializers
from core.models import Picture, TimePicture


class PictureSerializer(serializers.ModelSerializer):
    urls = serializers.URLField(source='get_absolute_url', read_only=True)
    owner = serializers.CharField(source='owner.user', read_only=True)

    class Meta:
        model = Picture
        fields = ['owner', 'name', 'urls', 'img']


class PictureAddSerializer(serializers.ModelSerializer):
    urls = serializers.URLField(source='get_absolute_url', read_only=True)
    owner = serializers.CharField(source='owner.user', read_only=True)

    class Meta:
        model = Picture
        fields = ['owner', 'name', 'urls', 'img']


class TimePictureSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url', read_only=True)
    picture = PictureSerializer(read_only=True)

    class Meta:
        model = TimePicture
        fields = ['url', 'picture', 'time', 'time_left']


class TimePictureShortSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url', read_only=True)
    picture = PictureSerializer(read_only=True, many=False)

    class Meta:
        model = TimePicture
        fields = ['url', 'picture', 'time']
