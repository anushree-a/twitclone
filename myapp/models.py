from django.db import models

class User(models.Model):
	user_id = models.AutoField(primary_key=True)
	email = models.EmailField(max_length=80, default="email")
	username = models.CharField(max_length=280, unique=True)
	password = models.CharField(max_length=2)
	isactive = models.BooleanField(default=False)

	def __str__(self):
		return str(self.username)

class Follow(models.Model):
	relation_id = models.AutoField(primary_key=True)
	follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_profile')
	followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followee_profile')

	def __str__(self):
		return str(self.relation_id)

class Tweet(models.Model):
	tweet_id = models.AutoField(primary_key=True)
	tweeter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tweeter_profile')
	tweet_content = models.CharField(max_length=280)
	num_likes = models.IntegerField(default=0)

	def __str__(self):
		return str(self.tweet_id)

class TweetActivity(models.Model):
	tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='tweet')
	activity_id = models.IntegerField(default=1)