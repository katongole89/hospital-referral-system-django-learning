from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='_login' ),
    re_path(r'^(?P<id>[0-9]+)/$', views.hosp_info, name='hosp_info' ),
    
] 