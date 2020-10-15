from django.db import models

from django.contrib.auth.models import User
from django.contrib.auth.models import User

# Create your models here.
'''
class Status(models.Model):
	status=models.CharField(max_length=20)
'''
class ToDoType(models.Model):
	todotype=models.CharField(max_length=20)

	def __str__(self):
		return self.todotype

class City(models.Model):
	city_name=models.CharField(max_length=20)

	def __str__(self):
		return self.city_name

class UserProfile(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)	
	city=models.ForeignKey(City,on_delete=models.SET_NULL,null=True)
	profpic=models.ImageField(upload_to='profpics')
	mobile=models.CharField(max_length=10)

class ToDoList(models.Model):
	title=models.CharField(max_length=45)
	created=models.DateTimeField(auto_now_add=True,editable=False,null=False,blank=False)
	userprof=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
	todotype=models.ForeignKey(ToDoType,on_delete=models.SET_NULL,null=True)
	status=models.ForeignKey(Status,on_delete=models.SET_NULL,null=True)
	textnote=models.CharField(max_length=5000,null=True)


class ToDoPoints(models.Model):
	todopoint=models.CharField(max_length=300)
	todolistid=models.ForeignKey(ToDoList,on_delete=models.CASCADE)
	#status=models.ForeignKey(Status,on_delete=models.SET_NULL,null=True,default=1)

class Connects(models.Model):
	from_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='from_connect')
	to_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='to_connect')
	status=models.ForeignKey(Status,on_delete=models.SET_NULL,null=True,default=4)
	