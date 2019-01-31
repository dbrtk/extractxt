

from django.urls import path

from . import views


urlpatterns = [

    path('', views.home, name='home'),

    path('upload-files/', views.upload_files, name='upload_files'),

]
