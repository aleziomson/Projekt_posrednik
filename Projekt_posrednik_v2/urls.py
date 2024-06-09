from django.contrib import admin
from django.urls import path, include
from Posrednik_v1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.initial_input, name='initial_input'),
    path('posrednik/initial/', views.initial_input, name='initial_input'),
    path('posrednik/calculate/', views.calculate, name='calculate'),
    path('posrednik/upload_file/', views.upload_file, name='upload_file'),
]


