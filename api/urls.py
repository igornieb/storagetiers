from django.urls import path, include
from api import views

urlpatterns = [
    path('pictures', views.PictureList.as_view(), name='picture-list'),
    path('pictures/shared', views.TimePictureList.as_view(), name='shared-picture-list'),
    path('picture/<uuid:pk>', views.PictureDetails.as_view(), name='picture-details'),
    path('picture/<uuid:pk>/<int:height>', views.PictureDetails.as_view(), name='picture-details'),
    path('timelink/<uuid:pk>', views.TimePictureDetails.as_view(), name='timelink'),
]
