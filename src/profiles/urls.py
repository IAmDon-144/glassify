from django.urls import path, include
from .views import myProfile,editMyProfile


urlpatterns = [


    path('my-profile/', myProfile, name='my-profile'),
    path('edit-profile/<pk>/edit/', editMyProfile, name='edit-profile'),




]
