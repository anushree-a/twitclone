from django.db import models

class User(models.Model):
	user_id = models.AutoField(primary_key=True)
	email = models.EmailField(max_length=80,unique=True, default="email")
	username = models.CharField(max_length=30, unique=True)
	password = models.CharField(max_length=20)
	isactive = models.BooleanField(default=False)

	def __str__(self):
		return str(self.username)