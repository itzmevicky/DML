from django.urls import path
from .views import *

urlpatterns = [
    path('',home),
    path('login/',loginView),
    path('register/',Register),
    path('logout/',logoutView),
    path('like/',likeView),
    path('dislike/',dlikeView)
]