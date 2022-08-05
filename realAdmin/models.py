from django.db import models
from login.models import Persons

# Create your models here.
class Hospitals(models.Model):
	hospital_name= models.CharField(max_length=40, blank= False)
	country= models.CharField(max_length= 40, blank=False)
	district= models.CharField(max_length= 40, blank=False)
	hospital_type= models.CharField(max_length= 40, blank=False)
	email= models.EmailField(max_length= 40, blank=True)
	phone_number=models.CharField(max_length= 40, blank=True)
	google_maps_url= models.CharField(max_length=400, blank=True)
	location=models.CharField(max_length=400, blank=True)

	def __str__(self):
		return self.hospital_name  + '--'+ self.country+ '--'+ self.district + '--'+ self.hospital_type

class speciality(models.Model):
	persons= models.ForeignKey(Persons, on_delete=models.CASCADE)
	hospitals= models.ForeignKey(Hospitals,on_delete=models.CASCADE, blank= True, null= True)
	spec1= models.CharField(max_length=30, blank=True)
	spec2= models.CharField(max_length=30, blank=True)
	spec3= models.CharField(max_length=30, blank=True)

	def __str__(self):
		return self.persons.nameUsed.username + '--'+ self.spec1+ '--'+ self.spec2 + '--'+ self.spec3

