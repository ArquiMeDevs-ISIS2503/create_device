from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    #path('devices/', views.device_list_),
    #path('deviceSede/', views.getSede),
    path('create_device/', csrf_exempt(views.device_create), name='deviceCreate'),
]