import json
import base64
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Follow, Tweet, TweetActivity
from django.contrib import messages
from django.core.mail import send_mail

@csrf_exempt 
def index(request):
    return HttpResponse("Hello world!")

#curl -X POST http://127.0.0.1:8000/myapp/register/ -d '{"email":"yourmail@gmail.com", username":"anushree", "password":"anushree"}' -H "Content-Type:application/json"
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
		return HttpResponse('Successful activation!')
	else:
		return JsonResponse({'result' : -1})


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

@csrf_exempt
#Nidhi's token = bmlkaGk=
#Sam's token = c2Ft
#Anushree's token = YW51c2g=
#curl -X POST http://127.0.0.1:8000/myapp/follow/ -d '{"follower": "bmlkaGk=", "followee":"c2Ft"}' -H "Content-Type:application/json"
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


@csrf_exempt
#Nidhi's token = bmlkaGk=
#Sam's token = c2Ft
#Anushree's token = YW51c2g=
#curl -X POST http://127.0.0.1:8000/myapp/unfollow/ -d '{"follower": "bmlkaGk=", "followee":"c2Ft"}' -H "Content-Type:application/json"
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

@csrf_exempt
#curl -X POST http://127.0.0.1:8000/myapp/createtweet/ -d '{"username": "YW51c2g=", "content":"My first tweet!"}' -H "Content-Type:application/json"
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

@csrf_exempt
#curl -X POST http://127.0.0.1:8000/myapp/deletetweet/ -d '{"tweet_id": "1"}' -H "Content-Type:application/json"
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


@csrf_exempt
#curl -X POST http://127.0.0.1:8000/myapp/readtweets/ -d '{"username": "bmlkaGk="}' -H "Content-Type:application/json"
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

@csrf_exempt
#curl -X POST http://127.0.0.1:8000/myapp/likeunlike/ -d '{"tweet_id": "6", "activity_id:"1}' -H "Content-Type:application/json"
def LikeUnlikeView(request):
	if request.method == 'POST':
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)
		tweet_id = body['tweet_id']
		activity_id = body['activity_id']

		temp_tweet = Tweet.objects.filter(tweet_id = tweet_id).first()
		print("content = ", temp_tweet.tweet_content)
		print("init num likes" , temp_tweet.num_likes)
		new_activity = TweetActivity.objects.create(tweet = temp_tweet, activity_id = activity_id)
		if(activity_id == '1'):
			temp_tweet.num_likes = temp_tweet.num_likes+1
			print("now num likes", temp_tweet.num_likes)
			temp_tweet.save()
			print("HEREE1")
		elif(activity_id == '2'):
			temp_tweet.num_likes= temp_tweet.num_likes-1
			print("now num likes", temp_tweet.num_likes)
			temp_tweet.save()
			print("HEREE2")
		new_activity.save()
		print('New activity recorded!')
		return JsonResponse({'result' : 1})
	else:
		return JsonResponse({'result' : -1})

@csrf_exempt
#curl -X POST http://127.0.0.1:8000/myapp/retweet/ -d '{"tweet_id": "6","username":"c2Ft"}' -H "Content-Type:application/json"
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
		return JsonResponse({'result' : 1})
	else:
		return JsonResponse({'result' : -1})
