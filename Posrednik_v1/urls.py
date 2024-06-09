from django.urls import path
from . import views

urlpatterns = [
    path('', views.initial_input, name='initial_input'),
    path('calculate/', views.calculate, name='calculate'),
    path('upload_file/', views.upload_file, name='upload_file'),
]
