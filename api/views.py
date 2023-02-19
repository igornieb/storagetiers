from django.http import Http404, HttpResponse
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Account, Picture
from api.serializers import *
from PIL import Image


# TODO create image link

class PictureList(APIView):
    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        account = Account.objects.get(user=self.request.user)
        pictures = Picture.objects.filter(owner=account)
        return pictures

    def get(self, request):
        pictures = self.get_queryset()
        serializer = PictureSerializer(pictures, many=True)
        return Response(serializer.data)

    def post(self, request):
        account = Account.objects.get(user=self.request.user)
        serializer = PictureSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(owner=account)
            return Response(serializer.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


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
            if 'original' in picture.get_sizes():
                return HttpResponse(picture.img, content_type="image/png")
            else:
                raise PermissionDenied({"message": "This picture cannot be displayed in its full resoution",
                                        "object": picture})
