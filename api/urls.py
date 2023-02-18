from django.urls import path, include
from api import views

urlpatterns = [
    path('pictures', views.PictureList.as_view(), name='picture-list'),
    path('picture/<pk>', views.PictureDetails.as_view(), name='picture-details')
    ]