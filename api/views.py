from django.http import Http404, HttpResponse
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from core.models import Account, Picture
from api.serializers import *
from PIL import Image


class PictureList(APIView):
    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        # returns list of Pictures that belong to given Account
        account = Account.objects.get(user=self.request.user)
        pictures = Picture.objects.filter(owner=account)
        return pictures

    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_headers("Authorization", ))
    def get(self, request):
        pictures = self.get_queryset()
        serializer = PictureSerializer(pictures, many=True)
        return Response(serializer.data)

    def post(self, request):
        account = Account.objects.get(user=self.request.user)
        serializer = PictureAddSerializer(data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save(owner=account)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PictureDetails(APIView):

    def get_permissions(self):
        return [permissions.IsAuthenticatedOrReadOnly()]

    def get_object(self, pk):
        try:
            return Picture.objects.get(pk=pk)
        except Picture.DoesNotExist:
            raise Http404

    def get_post_object(self, pk):
        try:
            user = Account.objects.get(user=self.request.user)
            return Picture.objects.get(pk=pk, owner=user)
        except Picture.DoesNotExist:
            raise Http404

    @method_decorator(cache_page(60 * 10))
    def get(self, request, pk, height=None):
        # returns image in given size
        picture = self.get_object(pk)
        if height:
            if height in picture.get_sizes():
                image = Image.open(picture.img)
                image.thumbnail((image.width, height), Image.ANTIALIAS)
                response = HttpResponse(content_type='image/jpg')
                if image.mode in ("RGBA", "P"):
                    image = image.convert("RGB")
                image.save(response, "JPEG")
                return response
            else:
                raise PermissionDenied({"message": "This picture cannot be displayed at this height",
                                        "object": picture})
        else:
            if picture.owner.tier.allow_original:
                return HttpResponse(picture.img, content_type="image/png")
            else:
                raise PermissionDenied({"message": "This picture cannot be displayed in its full resoution",
                                        "object": picture})

    def post(self, request, pk, height=None):
        # creates new TimePicture object
        picture = self.get_post_object(pk)
        serializer = TimePictureShortSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(picture=picture)
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TimePictureList(APIView):
    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        # returns list of TimePictures that belong to given Account
        account = Account.objects.get(user=self.request.user)
        pictures = TimePicture.objects.filter(picture__owner=account, expires__gt=timezone.now())
        return pictures

    def get(self, request):
        pictures = self.get_queryset()
        serializer = TimePictureSerializer(pictures, many=True)
        return Response(serializer.data)


class TimePictureDetails(APIView):
    def get_object(self, pk):
        try:
            return TimePicture.objects.get(pk=pk)
        except TimePicture.DoesNotExist:
            raise Http404

    @method_decorator(cache_page(60 * 10))
    def get(self, request, pk):
        # returns shared image or 404 if image is already expired
        time_picture = self.get_object(pk)
        time_picture.is_expired()
        if time_picture.expired is False:
            return HttpResponse(time_picture.picture.img, content_type="image/png")
        else:
            raise Http404
