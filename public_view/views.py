from django.shortcuts import render
from realAdmin.models import Hospitals,speciality


# Create your views here.

#showing all hospitals in the database
def index(request):
	all_hosp= Hospitals.objects.all()
	context={
		'all_hosp': all_hosp
	}
	return render(request, 'public_view/hospitals.html', context)

#showing all information for a particular hospital
def hosp_info(request, id):
	#query database and get hospital with a given id
	hospital= Hospitals.objects.get(id = id)

	#get all its doctors
	docs= speciality.objects.filter(hospitals= hospital)
	context={
		'hospital': hospital,
		'docs': docs
	}

	return render(request, 'public_view/hosp_info.html', context )
