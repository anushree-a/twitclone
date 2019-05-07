import json
import base64
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Follow
from django.contrib import messages
from django.core.mail import send_mail

@csrf_exempt 
def index(request):
    return HttpResponse("Hello world!")

#curl -X POST http://127.0.0.1:8000/myapp/register/ -d '{"email":"anush.abhyankar@gmail.com", username":"anushree", "password":"anushree"}' -H "Content-Type:application/json"
@csrf_exempt 
def RegistrationView(request):	
		if request.method == 'POST':
			body_unicode = request.body.decode('utf-8')
			body = json.loads(body_unicode)

			email = body['email']
			temp_email = User.objects.filter(email= email).first()
			if temp_email is not None:
				print('You already have an account under this email ID.')
				return JsonResponse({'result' : -1})

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

# curl -X POST http://127.0.0.1:8000/myapp/activate/ -d '{"email":"anush.abhyankar@gmail.com"}' -H "Content-Type:application/json"
# @csrf_exempt
# def ActivationView(request):
# 	if request.method == 'POST':
# 		body_unicode = request.body.decode('utf-8')
# 		body = json.loads(body_unicode)
# 		email = body['email']

# 		temp_user = User.objects.filter(email=email).first()
# 		temp_user.isactive = True;
# 		print(temp_user.username, 'activated.')
# 		temp_user.save()

# 		return JsonResponse({'result' : 1})
# 	else:
# 		return JsonResponse({'result' : -1})



#curl -X POST http://127.0.0.1:8000/myapp/activate/ -d '{"email":"anush.abhyankar@gmail.com"}' -H "Content-Type:application/json"
@csrf_exempt
def ActivationView(request,username):
	if request.method == 'GET':
		print(username)
		username = base64.b64decode(username).decode("utf8")
		temp_user = User.objects.filter(username=username).first()
		temp_user.isactive = True;
		print(temp_user.username, 'activated.')
		temp_user.save()

		return JsonResponse({'result' : 1})
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

		temp_user = User.objects.filter(username= username).first()

		if temp_user is not None:
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
			print('No such user in database.')
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



