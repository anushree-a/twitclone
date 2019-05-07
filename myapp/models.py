from django.db import models

class User(models.Model):
	user_id = models.AutoField(primary_key=True)
	email = models.EmailField(max_length=80,unique=True, default="email")
	username = models.CharField(max_length=30, unique=True)
	password = models.CharField(max_length=20)
	isactive = models.BooleanField(default=False)

	def __str__(self):
		return str(self.username)

class Follow(models.Model):
	relation_id = models.AutoField(primary_key=True)
	follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_profile')
	followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followee_profile')

	def __str__(self):
		return str(self.relation_id)
