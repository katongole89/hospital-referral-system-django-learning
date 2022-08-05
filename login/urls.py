from django.urls import path
from . import views
from doctor import views as doctor_views
from hospitalAdmin import views as hospitalAdmin_views
from realAdmin import views as realAdmin_views


urlpatterns = [
    path('', views._login, name='_login' ),
    path('success/',views.success, name= 'success'), 
    path('logout/', views._logout, name='_logout'),
    path('logged1/', doctor_views.index, name='doctor_logged'),
    path('logged2/', hospitalAdmin_views.index, name='hospitalAdmin_logged'),
    path('logged3/', realAdmin_views.ourDoctors, name='realAdmin_logged')  
] 