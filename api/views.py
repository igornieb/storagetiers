from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from core.models import Picture, Account
from api.serializers import *


# TODO add picture, picture details (links, etc)
class PictureList(ListAPIView):
    serializer_class = PictureSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        account = Account.objects.get(user=self.request.user)
        pictures = Picture.objects.filter(owner=account)
        return pictures
