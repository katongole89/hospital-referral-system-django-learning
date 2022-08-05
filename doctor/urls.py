from django.urls import path,re_path
from . import views

urlpatterns = [
    path('index/', views.index, name='index' ),
    path('settings/', views.settings, name='settings' ),
    path('make_referrals/', views.make_referrals, name='make_referrals' ),
    path('our_referrals/', views.our_referrals, name='our_referrals' ),
    path('edit_user/',views.edit_user, name='edit_user'),
    re_path(r'^(?P<id>[0-9]+)/$', views.accept, name='accept' ),
    path('password_change/',views.password_change, name='password_change'),
    re_path(r'^reTransfer/(?P<id>[0-9]+)/$', views.reTransfer, name='reTransfer' ),
    path('change_availability/',views.change_availability, name='change_availability'),
]
