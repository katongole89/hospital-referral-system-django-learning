from django.conf import settings as conf_settings
from django.shortcuts import render,redirect
from realAdmin.models import Hospitals,speciality
from .models import makeReferral
from hospitalAdmin.models import hospitalReferral
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from login.models import Persons
from django.core.mail import send_mail
from django.contrib.auth import update_session_auth_hash, authenticate
from .message import send_message
# Create your views here.

@login_required(login_url= '/login/')
def index(request):
	
	if request.method == "POST":
		#1
		#getting givven dat
		selected_special= request.POST.get('specialist')

		print(selected_special)
		#locations
		selected_district1= request.POST.get('location_1')
		selected_district2= request.POST.get('location_2')
		selected_district3= request.POST.get('location_3')
		selected_district4= request.POST.get('location_4')

		#2
		#querrying database ....looking objects with required specialities
		nigga= speciality.objects.filter(Q(spec1__iexact=selected_special) | Q(spec2__iexact=selected_special) | Q(spec3__iexact= selected_special))
		district_in= Hospitals.objects.filter(Q(district__iexact=selected_district1) | Q(district__iexact= selected_district2) | Q(district__iexact= selected_district3)| Q(district= selected_district4))

		#get hospital name using speciality

		print(nigga)
		print( district_in)


		#getting username of logged in user stored in session
		username = request.session.get('username')

		#3
		#create a list that will accomodate selected values from the looping 
		emptyNigga=[]

		#looping thru hospitals using the given districts
		for dis in district_in:
			#looping through doctors that belong to the above hospital
			for nig in nigga:
				thanos= User.objects.get(username= username)
				thanos2= Persons.objects.get(nameUsed= thanos)
				if thanos2 != nig.persons:
					print('True')
					f= nig.hospitals.district
					m= nig.hospitals.hospital_name
					if f== dis.district:
						if m not in emptyNigga:
							emptyNigga.append(m)

		print(emptyNigga)

		request.session['emptyNigga']= emptyNigga

		request.session['selected_special']= selected_special

		av= User.objects.get(username= username)
		av1= Persons.objects.get(nameUsed= av)

		#if they are there

		

		context={
		'emptyNigga': emptyNigga,
		'av1': av1
		}
		return render(request,'doctor/make_referrals.html', context)

	#4
	else:
		username = request.session.get('username')
		party= User.objects.get(username= username)
		welcome= Persons.objects.get(nameUsed= party)

		spec=['dentist', 'ears', 'legs', 'eyes', 'allergist', 'physician', 'neurologist', 'surgeon', 'radiologists','urologist','pathologists','dermatologist','oncologist','hermatologist','immunology','gynaecologist', 'psychiatrist']


		context={
			'welcome': welcome,
			'spec': spec
		}


		return render(request, 'doctor/index.html', context)



@login_required(login_url= '/login/')
def settings(request):
	#1
	#getting variable of username stored in the session
	username = request.session.get('username')

	#2
	#look for that ojects in the dataase where username is equal to the username of logged in user
	sett= User.objects.get(username= username)
	
	#3
	#list to contain all details of the user we want to display
	sett1=[]

	#4
	#adding the details
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
	'sett1': sett1,
	'sett2':sett2
	}

	return render(request, 'doctor/settings.html', context)

#editing user
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

	return redirect('/doctor/settings/')



	

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
		return redirect('/doctor/settings/')

	else:


		return redirect('/doctor/settings/')
		

	

# making a referral using the given patient information
@login_required(login_url= '/login/')
def make_referrals(request):

	#getting the hospitals that were stored in sessions from the previous page
	new_emptyNigga= request.session.get('emptyNigga')

	#getting the username of the logged in user that was stored in sessions
	username= request.session.get('username')

	selected_special= request.session.get('selected_special') 


	#saving the given infomation in the database

	patients_name= request.POST['patients_name']
	details= request.POST['details']
	patient_email= request.POST['patient_email']
	phone_number= request.POST['phone_number']

	#generating the referral code
	gen_code= makeReferral.objects.all().count()

	gen_code1= 'R' + str(gen_code+ 1)


	refer_doc= User.objects.get(username= username)


	new_ref= makeReferral( patient_name= patients_name, generated_code= gen_code1, email= patient_email,findings= details,  phone_number= phone_number, user=refer_doc )
	new_ref.save()

	_id= new_ref.id 

	for emp in new_emptyNigga:
		reff= Hospitals.objects.get(hospital_name__iexact= emp)

		reff1= speciality.objects.filter(hospitals=reff)

		madeRef= makeReferral.objects.get(id = _id )

		#doctors in the selected hospitals get this referral
		for r in reff1:
			if r.spec1== selected_special or r.spec2== selected_special or r.spec3== selected_special:
				if r.persons.nameUsed != madeRef.user:
					#referral doctor  must not see this information
					for_user= r.persons.nameUsed
					hospRef= hospitalReferral(madeReferral= madeRef, hospital_refer=reff , user= for_user)
					hospRef.save()

	spec=['dentist', 'ears', 'legs', 'eyes', 'allergist', 'physician', 'neurologist', 'surgeon', 'radiologists','urologist','pathologists','dermatologist','oncologist','hermatologist','immunology','gynaecologist', 'psychiatrist']

	context={
		'spec': spec
	}


	return render(request, 'doctor/index.html', context)

#showing referrals that require review
@login_required(login_url= '/login/')
def our_referrals(request):



	#determing the hospital of the doctor
	username = request.session.get('username')
	hos_connected= User.objects.get(username= username)
	hos1_connected= Persons.objects.get(nameUsed= hos_connected )

	hos2_connected= speciality.objects.get(persons= hos1_connected)
	hos3_connected= hos2_connected.hospitals.hospital_name

	ref= hospitalReferral.objects.all()

	#show only referrals for this hospital and that were referred to this logged in doctor
	for_display=[]
	for n in ref:
		if hos3_connected == n.hospital_refer.hospital_name and n.admin_approval==True and n.doctor_approval== False and n.status_of_referral==False and n.received==False :
			if n.user.username == username:
				for_display.append(n)


	context={
	'for_display': for_display,
	'hos1_connected': hos1_connected
	}
	return render(request, 'doctor/our_referrals.html', context)



#accepting a referral by the doctor
@login_required(login_url= '/login/')
def accept(request, id):
	#using the id of the referral
	#query database for referral with this id and update doctor approval to true 
	#this means patient has been accepted by  doctor
	hospitalReferral.objects.filter(id= id).update(doctor_approval= True)

	patient_info= hospitalReferral.objects.get(id= id)



	#sending message
	
	#message to sent
	message1='patient '+ patient_info.madeReferral.patient_name + ' with referral code '+ patient_info.madeReferral.generated_code + '. You have been referred to '+ patient_info.hospital_refer.hospital_name + ' hospital which is located in '+ patient_info.hospital_refer.district + ' .DETAILED LOCATION '+ patient_info.hospital_refer.location + ' OR you can go to the following link to find location on google maps  '+ patient_info.hospital_refer.google_maps_url
	#where it should e sent
	contact= [patient_info.madeReferral.phone_number]


	#send to the referring doctor
	ref_doctor= patient_info.madeReferral.user
	ref_doctor1= Persons.objects.get(nameUsed= ref_doctor)
	ref_doctor2= [ref_doctor1.phone_number]
	ref_doctor3= ref_doctor.email
	print(ref_doctor2)
	ref_message='Your patient '+ patient_info.madeReferral.patient_name+ ' from your hospital has been referred to '+ patient_info.hospital_refer.hospital_name + ' with referral code '+ patient_info.madeReferral.generated_code

	#send to referring hospital admin
	ref_ha= speciality.objects.get(persons= ref_doctor1)
	ref_ha1= ref_ha.hospitals
	ref_ha2= speciality.objects.filter(hospitals= ref_ha1)


	#send to hospital admins of the current hospital
	cur_ha= patient_info.hospital_refer
	cur_ha1= speciality.objects.filter(hospitals= cur_ha)

	cur_message= 'This message is to notify you that a new patient by the names '+patient_info.madeReferral.patient_name +' is ready to be received with referral code '+ patient_info.madeReferral.generated_code



	#catch the error
	#if there is an internet connection -----send the message
	try:
		#message is sent using africa is talking api
		import africastalking

		username = "kamogaedmund"
		api_key = "b9e82a793a16246c7627af8e5e2052ff32caec5b43872f4ec01b1ff41fe36ef9"

		africastalking.initialize(username, api_key)

		sms = africastalking.SMS
		response = sms.send(message1, contact)
		

	except Exception as e:
		pass

	finally:

		#catch error if there is no internet
		#sending an email
		try:
			#if the patient gave in an email ----send an email to it
			if patient_info.madeReferral.email is not None:
				subject = 'Referral Confirmed'
				message = 'patient '+ patient_info.madeReferral.patient_name + ' with referral code '+ patient_info.madeReferral.generated_code + '. You have been referred to '+ patient_info.hospital_refer.hospital_name + ' which is located in '+ patient_info.hospital_refer.district + ' .DETAILED LOCATION '+ patient_info.hospital_refer.location + '  OR you can go to the following link to find location on google maps  '+ patient_info.hospital_refer.google_maps_url
				email_from = conf_settings.EMAIL_HOST_USER
				recipient_list = [patient_info.madeReferral.email]
				send_mail( subject, message, email_from, recipient_list )
		except Exception as e:
			pass
		finally:
			#sending to the refering doctor
			try:
				send_message(ref_message, ref_doctor2)		
				
			except Exception as e:
				pass
			finally:
				try:
					subject = 'Referral Confirmed'
					message = ref_message
					email_from = conf_settings.EMAIL_HOST_USER
					recipient_list = [ref_doctor3]
					send_mail( subject, message, email_from, recipient_list )
				except Exception as e:
					raise
				else:
					pass
				finally:
					try:
						#sending to referring hospital admins
						for vv in ref_ha2:
							if not vv.spec1 and not vv.spec2 and not vv.spec3:
								ha_contact= [vv.persons.phone_number]
								print(ha_contact)
								send_message(ref_message, ha_contact)

					except Exception as e:
						pass
					finally:
						for vv in ref_ha2:
							if not vv.spec1 and not vv.spec2 and not vv.spec3:
								subject = 'Referral Confirmed'
								message = ref_message
								email_from = conf_settings.EMAIL_HOST_USER
								recipient_list = [vv.persons.nameUsed.email]
								send_mail( subject, message, email_from, recipient_list )

						try:
							#sending to the current hospital admins
							for xx in cur_ha1:
								if not xx.spec1 and not xx.spec2 and not xx.spec3:
									ha_contact= [xx.persons.phone_number]
									send_message(cur_message, ha_contact)

						except Exception as e:
							raise
						finally:
							try:
								for xx in cur_ha1:
									if not xx.spec1 and not xx.spec2 and not xx.spec3:
										subject = 'New Patient To Be Received'
										message = cur_message
										email_from = conf_settings.EMAIL_HOST_USER
										recipient_list = [xx.persons.nameUsed.email]
										send_mail( subject, message, email_from, recipient_list )

							
							except Exception as e:
								raise
							else:
								pass
							finally:
								k= hospitalReferral.objects.get(id= id)
								m= k.madeReferral
								p= hospitalReferral.objects.filter(madeReferral= m)

								for q in p:
									r=q.id
									if q != k:
										hospitalReferral.objects.filter(id= r).update(doctor_approval= True, status_of_referral=True)
								return HttpResponseRedirect(reverse('our_referrals'))


		

		

#Retransfering the patient
@login_required(login_url= '/login/')
def reTransfer(request, id):
	#using the given id of the referral
	#querry the database and get referral with that id
	ret= hospitalReferral.objects.get(id= id)
	ret1= ret.madeReferral

	ret2= hospitalReferral.objects.filter(madeReferral= ret1)

	#getting number of hospitals that the patient was referred to
	ret3=hospitalReferral.objects.filter(madeReferral= ret1).count()

	#if the patient was referred to many hospitals....then delete referral of that doctor who doesnt want
	if ret3>1:
		hospitalReferral.objects.filter(id= id).delete()
	#but if the patient was referred to only one hospital
	else:
		#just change admin approval to false such that the hospital admin of that hospital can see him again 
		#and resend him to that doctor wen he is ready
		hospitalReferral.objects.filter(id= id).update(status_of_referral=False, doctor_approval=False, admin_approval=False ,received=False)

	return HttpResponseRedirect(reverse('our_referrals'))

@login_required(login_url= '/login/')
def change_availability(request):
	#get username stored in session
	username = request.session.get('username')

	#get object from database with that username 
	party= User.objects.get(username= username)
	welcome= Persons.objects.get(nameUsed= party)

	#update the availability
	#if its true change it to false
	#if false change it to true
	if welcome.availablity == True:
		Persons.objects.filter(nameUsed= party).update(availablity= False)
	else:
		Persons.objects.filter(nameUsed= party).update(availablity= True)
	return redirect('/doctor/index')

		

