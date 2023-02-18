from django.http import Http404
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
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

class PictureDetails(APIView):
    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def get_object(self, pk):
        try:
            return Picture.objects.get(pk=pk)
        except Picture.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        picture = self.get_object(pk)
        serializer = PictureSerializer(picture, many=False)
        return Response(serializer.data)
