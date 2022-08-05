from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class makeReferral(models.Model):
	patient_name= models.CharField(max_length= 100, blank=False)
	findings= models.TextField(blank=True)
	
	"""scanned_documents"""
	email= models.EmailField(blank= True)
	referral_status= models.BooleanField(default=False)
	generated_code= models.CharField(max_length= 20)
	phone_number= models.CharField(max_length=20, blank= True)
	user= models.ForeignKey(User, on_delete=models.CASCADE,blank=True)
	

	def __str__(self):
		return self.patient_name+ '--'+ str(self.referral_status)+ '--'+ self.generated_code
