from rest_framework import serializers
from core.models import Picture


class PictureSerializer(serializers.ModelSerializer):
    urls = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Picture
        fields = ['owner', 'urls', 'get_sizes']
