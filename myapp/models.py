from django.db import models

#This stores the details about each TwitClone user
class User(models.Model):
	user_id = models.AutoField(primary_key=True)
	email = models.EmailField(max_length=80, default="email")
	username = models.CharField(max_length=280, unique=True)
	password = models.CharField(max_length=20)
	isactive = models.BooleanField(default=False)

	def __str__(self):
		return str(self.user_id)

#This stores details about follow relationships among users
class Follow(models.Model):
	relation_id = models.AutoField(primary_key=True)
	follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_profile')
	followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followee_profile')

	def __str__(self):
		return str(self.relation_id)

#This stores tweet details
class Tweet(models.Model):
	tweet_id = models.AutoField(primary_key=True)
	tweeter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tweeter_profile')
	tweet_content = models.CharField(max_length=280)
	num_likes = models.IntegerField(default=0)

	def __str__(self):
		return str(self.tweet_id)

#This stores tweet activity details(like/unlike/retweet)
class TweetActivity(models.Model):
	tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='tweet')
	activity_id = models.IntegerField(default=1)

	def __str__(self):
		return str(self.tweet_id)

#This stores tweet reply details
class TweetReply(models.Model):
	tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='tweett')
	replier = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replier')
	reply_content = models.CharField(max_length=280)

	def __str__(self):
		return str(self.replier)