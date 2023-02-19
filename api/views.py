from django.http import Http404, FileResponse, HttpResponse
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Picture, Account
from api.serializers import *
from PIL import Image


# TODO add picture, picture details (links, etc)
class PictureList(ListAPIView):
    serializer_class = PictureSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        account = Account.objects.get(user=self.request.user)
        pictures = Picture.objects.filter(owner=account)
        return pictures

class PictureDetails(APIView):
    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def get_object(self, pk):
        try:
            account = Account.objects.get(user=self.request.user)
            return Picture.objects.get(pk=pk, owner=account)
        except Picture.DoesNotExist:
            raise Http404

    def get(self, request, pk, height=None):
        picture = self.get_object(pk)
        if height:
            if height in picture.get_sizes():
                image = Image.open(picture.img)
                image.thumbnail((image.width,height), Image.ANTIALIAS)
                response = HttpResponse(content_type='image/jpg')
                image.save(response, "JPEG")
                return response
            else:
                raise PermissionDenied({"message": "This account doesnt have permisions to acces this link",
                                        "object": picture})
        else:
            if 'original' in picture.get_sizes():
                return HttpResponse(picture.img, content_type="image/png")
            else:
                raise PermissionDenied({"message": "This account doesnt have permisions to acces this link",
                                        "object": picture})


