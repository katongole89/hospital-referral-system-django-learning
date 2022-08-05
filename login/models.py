from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Persons(models.Model):
	nameUsed=models.ForeignKey(User, on_delete=models.CASCADE)
	role= models.CharField(max_length=50, blank=True)
	age= models.IntegerField(blank=True, null= True)
	availablity= models.BooleanField(null=True, blank= True)
	phone_number= models.CharField(max_length=20, blank= True)
	nin= models.CharField(max_length=30, blank=True)
	image= models.ImageField(blank= True, null= True)


	"""profile_pic= models.ImageField(upload_to= 'pic')"""
	
	def __str__(self):
		return self.nameUsed.username + '--'+ self.role+ '--'+ str(self.age)