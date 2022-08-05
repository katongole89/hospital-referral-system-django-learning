from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name='index' ),
    path('accept_patient/', views.accept_patient, name='accept_patient' ),
    re_path(r'^(?P<id>[0-9]+)/$', views.doctor_review, name='doctor_review' ),
    path('settings/', views.settings, name='settings' ),
    path('edit_user/',views.edit_user, name='edit_user'),
    re_path(r'^receive_patient/(?P<id>[0-9]+)/$', views.receive_patient, name='receive_patient' ),
    path('password_change/',views.password_change, name='password_change')
]