from django.shortcuts import render, redirect
from django.conf import settings as conf_settings
from django.core.mail import send_mail
from login.models import Persons
from django.contrib.auth.models import User
from .models import Hospitals, speciality
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from doctor.models import makeReferral
from django.contrib.auth import update_session_auth_hash, authenticate

# Create your views here.

#displaying all hospital admins
@login_required(login_url= '/login/')
def my_hospitalAdmins(request):
	#1
	#get all users from the dataase where role is hospital admin
	all_admin= Persons.objects.filter(role__exact='hospitalAdmin')
	

	#2
	#filtering information to display on template
	stuff=[]

	for doc in all_admin:
		all_stuff=[]
		_id= doc.id
		all_stuff.append(_id)
		f_name= doc.nameUsed.first_name
		all_stuff.append(f_name)
		l_name = doc.nameUsed.last_name
		all_stuff.append(l_name)
		availability= doc.availablity
		all_stuff.append(availability)
	
		sp= speciality.objects.get(persons__exact= doc)
		hosp= sp.hospitals.hospital_name
		all_stuff.append(hosp)

		stuff.append(all_stuff)


	context={
		'stuff': stuff
		}

	return render(request, 'realAdmin/hospitalAdmin.html', context)


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

def add_HospitalAdmin(request):
	#1
	#if there is informmation provided 
	if request.method=='POST':
		name= request.POST['name']
		username= request.POST['username']
		phone_number= request.POST['phone_number']
		email= request.POST['email']
		national_id_number= request.POST['national_id_number']
		
		hospital= request.POST.get('hospital')

		#Auto generating password --creating a random password using the random module to randomly pick characters
		import random
		x=4
		letter_part=''
		#loop the statements below until x not greater than 0
		while x>0:
			choose_from=['a','b','c','d','e','g','h','j','k','m','n','p','q','s','t','v','w','x','y','z']
			rd= random.choice(choose_from)
			letter_part=rd + letter_part
			rt= random.randint(0,9)
			letter_part= str(rt)+ letter_part

			x= x-1


		hospi= Hospitals.objects.all()

		#catching error if user is already there in the system
		try:
			user_already_thea= User.objects.get(username= username)
			if user_already_thea:
				nigga='username is already thea'
				context={
					'nigga': nigga,
					'hospi': hospi
				}
				return render(request, 'realAdmin/add_HospitalAdmin.html', context)

		#if the user is not there then add him to the system
		except Exception as e:

			#adding User to the database
			query= User(username= username, first_name= name , email = email )
			query.save()

			setting_password= User.objects.get(username= username)
			setting_password.set_password(letter_part)
			setting_password.save()

			get_id= User.objects.get(username__exact= username)
			query2= Persons(nameUsed= get_id, nin= national_id_number, role='hospitalAdmin' ,availablity= False, phone_number= phone_number )
			query2.save()

			get_id2= Persons.objects.get(nameUsed= get_id)

			hosp= Hospitals.objects.get(hospital_name__exact= hospital)



			query3= speciality(persons=get_id2, hospitals= hosp )
			query3.save()

			#send email if there is an internet connection
			try:
				#sending email
				subject = 'Addition to the Health Referral System'
				message = 'This is to notify you that hospital admin '+ name +' ,You have been added to the Health Referral System with username '+ username + ' and password '+ letter_part
				email_from = conf_settings.EMAIL_HOST_USER
				recipient_list = [email]
				send_mail( subject, message, email_from, recipient_list )
				
			except Exception as e:
				pass
			finally:
				return HttpResponseRedirect(reverse('my_hospitalAdmins'))

	else:
		#generating random password
		import random
		x=4
		letter_part=''
		while x>0:
			choose_from=['a','b','c','d','e','g','h','j','k','m','n','p','q','s','t','v','w','x','y','z']
			rd= random.choice(choose_from)
			letter_part=rd + letter_part
			rt= random.randint(0,9)
			letter_part= str(rt)+ letter_part
			x= x-1

		hospi= Hospitals.objects.all()

		context={
			"letter_part":letter_part,
			'hospi': hospi
		}
		return render(request, 'realAdmin/add_HospitalAdmin.html', context)

@login_required(login_url= '/login/')
def ourDoctors(request):

	#query the persons table and get all users with role doctor
	all_doctors= Persons.objects.filter(role__exact='doctor')
	
	#refining to get required information
	stuff=[]
	for doc in all_doctors:
		all_stuff=[]
		_id= doc.id
		all_stuff.append(_id)
		f_name= doc.nameUsed.first_name
		all_stuff.append(f_name)
		l_name = doc.nameUsed.last_name
		all_stuff.append(l_name)
		availability= doc.availablity
		all_stuff.append(availability)

		
	
		sp= speciality.objects.filter(persons__exact= doc)

		for spec4 in sp:

			sp1= spec4.spec1
			sp2= spec4.spec2
			sp3= spec4.spec3
			hosp= spec4.hospitals.hospital_name

			all_stuff.append(sp1)
			all_stuff.append(sp2)
			all_stuff.append(sp3)
			all_stuff.append(hosp)

			stuff.append(all_stuff)


	context={
		'stuff': stuff
		}

	return render(request, 'realAdmin/my_doctors.html', context)

@login_required(login_url= '/login/')
def delete_doctor(request,id):
	del_doc= Persons.objects.get(id= id)
	del_doc1= del_doc.nameUsed.id
	del_doc2= User.objects.filter(id= del_doc1).delete()

	return redirect('/realAdmin/ourDoctors/')

@login_required(login_url= '/login/')
def delete_hospital_admin(request,id):
	del_doc= Persons.objects.get(id= id)
	del_doc1= del_doc.nameUsed.id
	del_doc2= User.objects.filter(id= del_doc1).delete()

	return redirect('/realAdmin/my_hospitalAdmins/')

@login_required(login_url= '/login/')
def addDoctor(request):
	if request.method=='POST':

		#getting all information and storing it in variables
		name= request.POST['name']
		username= request.POST['username']
		phone_number= request.POST['phone_number']
		email= request.POST['email']
		national_id_number= request.POST['national_id_number']
		speciality_1= request.POST.get('speciality_1')
		speciality_2= request.POST.get('speciality_2')
		speciality_3= request.POST.get('speciality_3')
		hospital= request.POST.get('hospital')

		#generating random password
		import random
		x=4
		letter_part=''
		while x>0:
			choose_from=['a','b','c','d','e','g','h','j','k','m','n','p','q','s','t','v','w','x','y','z']
			rd= random.choice(choose_from)
			letter_part=rd + letter_part
			rt= random.randint(0,9)
			letter_part= str(rt)+ letter_part
			x= x-1

		#querying database to get all hospitals
		hospi= Hospitals.objects.all()

		#catch error----if the user is already there
		try:
			user_already_thea= User.objects.get(username= username)
			if user_already_thea:
				nigga='username is already thea'
				context={
					'nigga': nigga,
					'hospi': hospi
				}
				return render(request, 'realAdmin/add_doctor.html', context)

		#if not there
		except Exception as e:


			#adding the user to the database
			query= User(username= username, first_name= name , email = email )
			query.save()

			setting_password= User.objects.get(username= username)
			setting_password.set_password(letter_part)
			setting_password.save()

			get_id= User.objects.get(username__exact= username)

			query2= Persons(nameUsed= get_id, nin= national_id_number, role='doctor' ,availablity= False, phone_number= phone_number)
			query2.save()

			get_id2= Persons.objects.get(nameUsed= get_id)

			hosp= Hospitals.objects.get(hospital_name__exact= hospital)



			query3= speciality(persons=get_id2, spec1=speciality_1, spec2= speciality_2, spec3= speciality_3, hospitals= hosp )
			query3.save()

			try:
				#sending email to the given email to tell them they have been added to the system
				subject = 'Addition to the Health Referral System'
				message = 'This is to notify you that Dr '+ name +' ,You have been added to the Health Referral System with username '+ username+ ' and password '+ letter_part
				email_from = conf_settings.EMAIL_HOST_USER
				recipient_list = [email]
				send_mail( subject, message, email_from, recipient_list )
				
			except Exception as e:
				pass
			finally:
				return HttpResponseRedirect(reverse('ourDoctor'))

	else:

		#generating random password
		import random
		x=4
		letter_part=''
		while x>0:
			choose_from=['a','b','c','d','e','g','h','j','k','m','n','p','q','s','t','v','w','x','y','z']
			rd= random.choice(choose_from)
			letter_part=rd + letter_part
			rt= random.randint(0,9)
			letter_part= str(rt)+ letter_part
			x= x-1

		#querying dataase to get all hospital objects
		hospi= Hospitals.objects.all()

		spec=['dentist', 'ears', 'legs', 'eyes', 'allergist', 'physician', 'neurologist', 'surgeon', 'radiologists','urologist','pathologists','dermatologist','oncologist','hermatologist','immunology','gynaecologist', 'psychiatrist']


		context={
			"letter_part":letter_part,
			'hospi': hospi,
			'spec': spec
		}
		return render(request, 'realAdmin/add_doctor.html', context)
	

#showing all hospitals
@login_required(login_url= '/login/')
def my_hospitals(request):
	#query the hospitals table and get all hospitals registered and store the result in nhospitals
	nhospitals= Hospitals.objects.all()
	
	context={
	"nhospitals" : nhospitals
	}
	return render(request, 'realAdmin/my_hospitals.html', context)

@login_required(login_url= '/login/')
def addHospital(request):
	if request.method== 'POST':

		#getting all input user information and storing it in variables
		hospital_name= request.POST['hospital_name']
		country= request.POST.get('country')
		district=  request.POST.get('district')
		hosp_type= request.POST.get('type')
		email= request.POST['email']
		phone_number= request.POST['phone_number']
		location= request.POST['location']
		google_maps_url= request.POST['google_maps_url']


		#checking if the hospital with that hospital name is there
		try:
			w= Hospitals.objects.get(hospital_name= hospital_name)
			if w:
				ryt='Hospital name is already there'
				context={
					'ryt': ryt
				}
				return render(request, 'realAdmin/add_hospital.html' ,context)
		
		#if its not there then add it to the system
		except Exception as e:
			
		
			#saving hospital to the system
			hospi= Hospitals(hospital_name= hospital_name, country= country , district= district, hospital_type= hosp_type, location=location, google_maps_url=google_maps_url, email=email, phone_number=phone_number )
			hospi.save()

			#if there is an internet connection .....send an email to the given email
			try:
				#sending email to the given email
				subject = 'Your Hospital '+ hospital_name + ' has been added '
				message = 'This is to notify you that '+ hospital_name + ' hospital has been added to the Health Referral system.'
				email_from = conf_settings.EMAIL_HOST_USER
				recipient_list = [email]
				send_mail( subject, message, email_from, recipient_list )

			except Exception as e:
				pass
			finally:
				return HttpResponseRedirect(reverse('my_hospitals'))

	return render(request, 'realAdmin/add_hospital.html')

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

	return render(request, 'realAdmin/settings.html', context)

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

	return redirect('/realAdmin/settings/')

@login_required(login_url= '/login/')
def delete_hospital(request, id):
	#determining its all doctors to be deleted
	docs_d=Hospitals.objects.get(id= id)
	print(docs_d)
	docs_d1= speciality.objects.filter(hospitals= docs_d)
	print(docs_d1)
	for nn in docs_d1:
		k=nn.persons.nameUsed.username
		User.objects.filter(username= k).delete()

	Hospitals.objects.filter(id= id).delete()
	return HttpResponseRedirect(reverse('my_hospitals'))

#method for showing all patients that are registered in the system
@login_required(login_url= '/login/')
def all_patients(request):
	#query dataase for all patients
	all_p= makeReferral.objects.all()

	context={
		'all_p': all_p
	}

	return render(request, 'realAdmin/all_patients.html', context)