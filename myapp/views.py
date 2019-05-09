import json
import base64
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Follow, Tweet, TweetActivity, TweetReply
from django.contrib import messages
from django.core.mail import send_mail

#This view is simply for testing out if the project is running in the initial stages of the project.
@csrf_exempt 
def index(request):
    return HttpResponse("Hello world!")

#This view handles the stage-1 of the user registration process - ie getting user informationa and sending a verification email to the user.
#Input --> email, username, password
#Output --> 1 if success, -1 if failure
#curl -X POST http://127.0.0.1:8000/myapp/register/ -d '{"email":"yourmail@gmail.com", "username":"anushree", "password":"anushree"}' -H "Content-Type:application/json"
@csrf_exempt 
def RegistrationView(request):	
		if request.method == 'POST':
			body_unicode = request.body.decode('utf-8')
			body = json.loads(body_unicode)

			email = body['email']
			username = body['username']
			temp_username = User.objects.filter(username= username).first()
			if temp_username is not None:
				print('This username already exists in our database! Please try another username.')
				return JsonResponse({'result' : -1})

			password = body['password']
			user_obj=User.objects.create(email=email,username=username, password=password)
			user_obj.save()

			if user_obj is not None:
				base64username = base64.b64encode( bytes(username, "utf-8") )
				base64username_string = base64username.decode("utf-8")
				print('Success!')
				email_subject = "Welcome to TwitClone!"
				email_from = "anush.abhyankar@gmail.com"
				email_to = [user_obj.email]
				email_content = "Hello there! Thanks for joining the TwitClone Community!\n\nPlease click on this link to activate your account: http://127.0.0.1:8000/myapp/activate/"+base64username_string
				x = send_mail(subject = email_subject, from_email = email_from, recipient_list = email_to, message = email_content, fail_silently=False)
				return JsonResponse({'result' : 1})
			else:
				print('There was an error. :(')
				return JsonResponse({'result' : -1})
		else:
			print('There was an error. :(')
			return JsonResponse({'result' : -1})

#This view handles the stage-2 of the user registration process - ie activating the account by setting isactive to True
#Input --> None 
#Output --> A HTTP response which says 'Account activated successfully!' if success else -1.
#curl -X POST http://127.0.0.1:8000/myapp/activate/ -d '{"email":"yourmail@gmail.com"}' -H "Content-Type:application/json"
@csrf_exempt
def ActivationView(request,username):
	if request.method == 'GET':
		print(username)
		username = base64.b64decode(username).decode("utf8")
		temp_user = User.objects.filter(username=username).first()
		temp_user.isactive = True;
		print(temp_user.username, 'activated.')
		temp_user.save()
		return HttpResponse('Account activated successfully!')
	else:
		return JsonResponse({'result' : -1})


#This view handles the login process. 
#Input --> username, password
#Output --> 64-bit encoded username token if success else -1
#curl -X POST http://127.0.0.1:8000/myapp/login/ -d '{"username": "anushree", "password":"anushree"}' -H "Content-Type:application/json"
@csrf_exempt
def LoginView(request):
	if request.method == 'POST':
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)
		username = body['username']
		password = body['password']

		temp_user = User.objects.filter(username= username,password=password).first()

		if temp_user is not None:
			if temp_user.isactive is False:
				print('Account hasn\'t been activated yet!')
				return JsonResponse({'user_token' : -1})

			base64username = base64.b64encode( bytes(username, "utf-8") )
			base64username_string = base64username.decode("utf-8")
			if temp_user.password == password:
				print('Hello' , username)
				print(base64username_string)
				return JsonResponse({'user_token' : base64username_string})
			else:
				print('Wrong password entered!')
				return JsonResponse({'user_token' : -1})
		else:
			print('Wrong username or password.')
			return JsonResponse({'user_token' : -1})
	else:
		return JsonResponse({'user_token' : -1})

#This view handles the follow operation. 
#Input --> follower and followee (in 64-bit encoded form)
#Output --> 1 if success else -1
#curl -X POST http://127.0.0.1:8000/myapp/follow/ -d '{"follower": "bmlkaGk=", "followee":"c2Ft"}' -H "Content-Type:application/json"
@csrf_exempt
def FollowView(request):
	if request.method == 'POST':
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)
		follower = body['follower']
		follower = base64.b64decode(follower).decode("utf8")
		followee = body['followee']
		followee = base64.b64decode(followee).decode("utf8")

		followerUser_obj = User.objects.filter(username=follower).first()
		followeeUser_obj = User.objects.filter(username=followee).first()
		pre_existance_flag = Follow.objects.filter(follower = followerUser_obj, followee = followeeUser_obj).exists()
		print("Pre-existance -->",pre_existance_flag)
		if(pre_existance_flag == False):
			new_relation = Follow(follower = followerUser_obj, followee=followeeUser_obj)
			new_relation.save()
		print('Follow operation successful.')
		return JsonResponse({'result' : 1})
	else:
		return JsonResponse({'result' : -1})


#This view handles the unfollow operation.
#Input --> follower and followee (in 64-bit encoded form)
#Output --> 1 if success else -1
#curl -X POST http://127.0.0.1:8000/myapp/unfollow/ -d '{"follower": "bmlkaGk=", "followee":"c2Ft"}' -H "Content-Type:application/json"
@csrf_exempt
def UnfollowView(request):
	if request.method == 'POST':
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)
		follower = body['follower']
		follower = base64.b64decode(follower).decode("utf8")
		followee = body['followee']
		followee = base64.b64decode(followee).decode("utf8")

		followerUser_obj = User.objects.filter(username=follower).first()
		followeeUser_obj = User.objects.filter(username=followee).first()
		Follow.objects.filter(follower = followerUser_obj, followee = followeeUser_obj).delete()
		print('Unfollow operation successful.')
		return JsonResponse({'result' : 1})
	else:
		return JsonResponse({'result' : -1})

#This view handles tweet creation operation
#Input --> username (in 64-bit encoded form), tweet content
#Output --> 1 if success else -1 
#curl -X POST http://127.0.0.1:8000/myapp/createtweet/ -d '{"username": "YW51c2g=", "content":"My first tweet!"}' -H "Content-Type:application/json"
@csrf_exempt
def CreateTweet(request):
	if request.method == 'POST':
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)
		username = body['username']
		username = base64.b64decode(username).decode("utf8")
		content = body['content']

		temp_user = User.objects.filter(username=username).first()
		new_tweet = Tweet(tweeter = temp_user, tweet_content=content)
		new_tweet.save()
		print(username, 'has tweeted successfully!')
		return JsonResponse({'result' : 1})
	else:
		return JsonResponse({'result' : -1})

#This view handles tweet deletion operation
#Input --> tweet_id
#Output --> 1 if success else -1 
#curl -X POST http://127.0.0.1:8000/myapp/deletetweet/ -d '{"tweet_id": "1"}' -H "Content-Type:application/json"
@csrf_exempt
def DeleteTweet(request):
	if request.method == 'POST':
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)
		tweet_id = body['tweet_id']

		temp_tweet = Tweet.objects.filter(tweet_id=tweet_id).delete()
		print('Tweet deleted_ successfully!')
		return JsonResponse({'result' : 1})
	else:
		return JsonResponse({'result' : -1})


#This view handles tweet deletion operation
#Input --> username(in encoded format)
#Output --> list of tweets if success else -1 
#curl -X POST http://127.0.0.1:8000/myapp/readtweets/ -d '{"username": "bmlkaGk="}' -H "Content-Type:application/json"
@csrf_exempt
def ReadTweets(request):
	if request.method == 'POST':
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)
		username = body['username']
		username = base64.b64decode(username).decode("utf8")
		temp_user = User.objects.filter(username=username).first()
		tweets = Tweet.objects.filter(tweeter = temp_user)
		tweets_content = []
		for t in tweets:
			tweets_content.append(t.tweet_content)
		return JsonResponse({'tweets' : tweets_content})
	else:
		return JsonResponse({'result' : -1})

#This view handles the like or dislike operation
#Input --> tweet_id, activity_id (1 for like, 2 for dislike)
#Output --> 1 if success else -1
#curl -X POST http://127.0.0.1:8000/myapp/likeunlike/ -d '{"tweet_id": "6", "activity_id":"1"}' -H "Content-Type:application/json"
@csrf_exempt
def LikeUnlikeView(request):
	if request.method == 'POST':
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)
		tweet_id = body['tweet_id']
		activity_id = body['activity_id']

		temp_tweet = Tweet.objects.filter(tweet_id = tweet_id).first()
		new_activity = TweetActivity.objects.create(tweet = temp_tweet, activity_id = activity_id)
		if(activity_id == '1'):
			temp_tweet.num_likes = temp_tweet.num_likes+1
			temp_tweet.save()
		elif(activity_id == '2'):
			temp_tweet.num_likes= temp_tweet.num_likes-1
			temp_tweet.save()
		new_activity.save()
		print('New activity recorded!')
		return JsonResponse({'result' : 1})
	else:
		return JsonResponse({'result' : -1})

#This view handles the retweet functionality
#Input --> tweet_id, your own username (in 64-bit encoded form)
#Output --> 1 if success else -1
#curl -X POST http://127.0.0.1:8000/myapp/retweet/ -d '{"tweet_id": "6","username":"c2Ft"}' -H "Content-Type:application/json"
@csrf_exempt
def RetweetView(request):
	if request.method == 'POST':
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)
		tweet_id = body['tweet_id']
		username = body['username']
		username = base64.b64decode(username).decode("utf8")

		temp_tweet = Tweet.objects.filter(tweet_id=tweet_id).first()
		tweet_content = temp_tweet.tweet_content
		temp_user = User.objects.filter(username=username).first()
		new_tweet = Tweet(tweeter = temp_user, tweet_content=tweet_content)
		new_tweet.save()
		print(username, 'has retweeted successfully!')
		new_activity = TweetActivity.objects.create(tweet = new_tweet, activity_id = 3)
		new_activity.save()
		print('New activity recorded!')
		return JsonResponse({'result' : 1})
	else:
		return JsonResponse({'result' : -1})

#This view handles the functionality to reply to tweets
#Input --> tweet_id, your own username (in 64-bit encoded form), reply content
#Output --> 1 if success else -1
#curl -X POST http://127.0.0.1:8000/myapp/replytweet/ -d '{"tweet_id": "6","username":"c2Ft", "reply_content":"Nice!"}' -H "Content-Type:application/json"
@csrf_exempt
def ReplyView(request):
	if request.method == 'POST':
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)
		tweet_id = body['tweet_id']
		username = body['username']	
		username = base64.b64decode(username).decode("utf8")
		reply_content = body['reply_content']

		temp_tweet = Tweet.objects.filter(tweet_id=tweet_id).first()
		temp_user = User.objects.filter(username=username).first()

		new_reply = TweetReply(tweet = temp_tweet, reply_content = reply_content, replier = temp_user)
		new_reply.save()
		print(new_reply.reply_content)
		print(username, 'replied!')
		return JsonResponse({'result' : 1})
	else:
		return JsonResponse({'result' : -1})
