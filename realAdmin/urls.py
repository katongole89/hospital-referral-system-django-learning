from django.urls import path, re_path
from . import views


urlpatterns = [
    path('ourDoctors/', views.ourDoctors, name='ourDoctor' ),
    path('my_hospitals/', views.my_hospitals, name='my_hospitals' ),
    path('addDoctor/', views.addDoctor, name='addDoctor' ),
    path('addHospital/', views.addHospital, name='addHospital' ),
   	path('settings/', views.settings, name='settings' ),
   	re_path(r'^(?P<id>[0-9]+)/$', views.delete_hospital, name='delete_hospital' ),
   	path('my_hospitalAdmins/', views.my_hospitalAdmins, name='my_hospitalAdmins' ),
   	path('add_HospitalAdmin/', views.add_HospitalAdmin, name='add_HospitalAdmin' ),
   	path('edit_user/',views.edit_user, name='edit_user'),
   	path('all_patients/',views.all_patients, name='all_patients'),
    path('password_change/',views.password_change, name='password_change'),
    re_path(r'^delete_doctor/(?P<id>[0-9]+)/$', views.delete_doctor, name='delete_doctor' ),
    re_path(r'^delete_hospital_admin/(?P<id>[0-9]+)/$', views.delete_hospital_admin, name='delete_hospital_admin' )

   
]