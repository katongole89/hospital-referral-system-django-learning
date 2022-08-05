from django.db import models
from doctor.models import makeReferral
from realAdmin.models import Hospitals
from django.contrib.auth.models import User

# Create your models here.
class hospitalReferral(models.Model):
	madeReferral=models.ForeignKey(makeReferral, on_delete=models.CASCADE)
	# needs changing from one to many relationship
	hospital_refer=models.ForeignKey(Hospitals, on_delete=models.CASCADE)
	
	#when the patient is received  its true
	status_of_referral= models.BooleanField(default= False)

	doctor_approval= models.BooleanField(default= False)

	admin_approval= models.BooleanField(default= False)

	received= models.BooleanField(default= False)

	user= models.ForeignKey(User,on_delete=models.CASCADE)

	def __str__(self):
		return self.madeReferral.patient_name+ '--'+ self.hospital_refer.hospital_name+ '--'+ str(self.status_of_referral) 

