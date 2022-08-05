from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Persons
from django.contrib.auth.decorators import login_required

# Create your views here

#show login page
def _login(request):
	return render(request, 'login/login.html')


#checking database for the information given and login user
def success(request):
	context={}
	if request.method == "POST":
		#get username and password given by the user and store them in variables
		username= request.POST['username']
		password= request.POST['password']

		#check if user is there in the database
		user= authenticate(request, username= username, password= password)
		
		#if the user is there login the user
		if user:

			login(request, user)
			f= User.objects.filter(username= username)
			k= f[0]
			n=k.id
			c=Persons.objects.filter(nameUsed__exact= n )
			z=c[0]
			d=z.role

			request.session['username']= username

			#return pages basing on the role of the logged in user
			if d == 'doctor':
				return HttpResponseRedirect(reverse('doctor_logged'))
			elif d== 'hospitalAdmin':
				return HttpResponseRedirect(reverse('hospitalAdmin_logged'))
			else:
				return HttpResponseRedirect(reverse('realAdmin_logged'))

		else:
			context['error']= 'provide valid credentials'
			return render(request, 'login/login.html' ,context )

#logging out user
@login_required(login_url= '/login/')
def _logout(request):
	#log out user
	logout(request)
	return redirect('/login/')
	