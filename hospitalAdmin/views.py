from django.shortcuts import render, redirect
from .models import hospitalReferral
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from login.models import Persons
from realAdmin.models import Hospitals,speciality
from django.contrib.auth import update_session_auth_hash, authenticate

# Create your views here.


#showing all patients that are already to be received
@login_required(login_url= '/login/')
def index(request):

	#quering database from the hospitalReferral table and get all referrals and store them in ready receive
	ready_receive= hospitalReferral.objects.all()

	#refining infomation to be displayed on website

	ready_accept=[]

	#looping through hospital referrals
	for ac in ready_receive:
		#checking if a given referral of a patient has been accepted by doctor 
		if ac.status_of_referral == False and ac.doctor_approval== True and ac.admin_approval==True and ac.received== False:
			username = request.session.get('username')
			hos_connected= User.objects.get(username= username)
			hos1_connected= Persons.objects.get(nameUsed= hos_connected )
			hos2_connected= speciality.objects.get(persons= hos1_connected)
			hos3_connected= hos2_connected.hospitals.hospital_name

			hos4_connected= ac.hospital_refer.hospital_name

			# to add the ac object to refined list ready_accept....the hospital of referral must be same as that of the logged in hospital admin
			if hos3_connected== hos4_connected:
				ready_accept.append(ac)

	context= {
	'ready_accept': ready_accept
	}

	return render(request, 'hospitalAdmin/index.html' , context)

@login_required(login_url= '/login/')
def password_change(request):
	passw = request.session.get('username')
	pass1= request.POST['pass1']
	pass2= request.POST['pass2']

	f= User.objects.get(username= passw)
	if pass1== pass2:
		f.set_password(pass1)
		user=f.save()
	
		update_session_auth_hash(request, user)
		return redirect('/realAdmin/settings/')

	else:


		return redirect('/realAdmin/settings/')

#showing patients that require doctors review----meaning they need to be sent to the doctor
@login_required(login_url= '/login/')
def accept_patient(request):
	#query and get all hospital referrals
	accepted= hospitalReferral.objects.all()
	
	#refining information that will be displayed on the template
	require_accept=[]
	for acc in accepted:
		#get only referrals that havent been accepted by hospital admins 
		if acc.status_of_referral != True and acc.admin_approval != True and acc.doctor_approval != True and acc.received== False:
			username = request.session.get('username')
			hos_connected= User.objects.get(username= username)
			hos1_connected= Persons.objects.get(nameUsed= hos_connected )
			hos2_connected= speciality.objects.get(persons= hos1_connected)
			hos3_connected= hos2_connected.hospitals.hospital_name

			hos4_connected= acc.hospital_refer.hospital_name

			#get only referral for that given hospital
			#hospital of referral must be same as hospital of hospital admin
			if hos3_connected== hos4_connected:

				#adding refined information to list that will be used in template
				doctor=[]
				doc_work= acc.user
				doc_work1= Persons.objects.get(nameUsed= doc_work)
				doc_work2= doc_work1.availablity
				doctor.append(doc_work2)

				pat_name= acc.madeReferral.patient_name
				doctor.append(pat_name)

				gen_code= acc.madeReferral.generated_code
				doctor.append(gen_code)

				doc_name= acc.user.first_name
				doctor.append(doc_name)

				ref_id= acc.id
				doctor.append(ref_id)

				require_accept.append(doctor)

	context= {
	'require_accept': require_accept
	}

	return render(request, 'hospitalAdmin/accept_patient.html' , context)


@login_required(login_url= '/login/')
def settings(request):
	username = request.session.get('username')
	sett= User.objects.get(username= username)
	sett1=[]

	nam= sett.first_name
	sett1.append(nam)
	nam1=sett.last_name
	sett1.append(nam1)
	nam2=sett.username
	sett1.append(nam2)
	nam3=sett.email
	sett1.append(nam3)

	sett2= Persons.objects.get(nameUsed= sett)

	nam4= sett2.role
	sett1.append(nam4)
	nam5= sett2.phone_number
	sett1.append(nam5)
	nam6= sett2.nin
	sett1.append(nam6)


	context={
	'sett1': sett1
	}

	return render(request, 'hospitalAdmin/settings.html', context)

@login_required(login_url= '/login/')
def edit_user(request):
	name= request.POST['name']
	username= request.POST['username']
	phone_number= request.POST['phone_number']
	email= request.POST['email']

	xx = request.session.get('username')


	delete_last=User.objects.get(username= xx)
	if delete_last.last_name:
		User.objects.filter(username= xx).update(last_name= '  ')


	edit_users= User.objects.filter(username= xx).update(username= username, first_name= name, email=email )
	xs= User.objects.get(username= username)

	Persons.objects.filter(nameUsed=xs).update(phone_number= phone_number)

	request.session['username']= username

	return redirect('/hospitalAdmin/settings/')

#sending a particular referral to doctor for review 
@login_required(login_url= '/login/')
def doctor_review(requset, id):
	#using the id of the referral
	#update admin approval to true so that its ready for review by doctor
	hospitalReferral.objects.filter( id= id ).update(admin_approval= True)
	return redirect('/hospitalAdmin/accept_patient/')
	


#receive patient that have been accepted the doctors
@login_required(login_url= '/login/')
def receive_patient(request, id):
	#using the id of the referral
	#update status of referal to true and received to true meaning they have been worked on 
	hospitalReferral.objects.filter( id= id ).update(status_of_referral=True, received= True)
	return redirect('/hospitalAdmin/')
