import json
import base64
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User

@csrf_exempt 
def index(request):
    return HttpResponse("Hello, world. You're safe. Everything's working.")

#curl -X POST http://127.0.0.1:8000/myapp/register -d '{"username":"anushree", "password":"anushree"}' -H "Content-Type:application/json"
@csrf_exempt 
def RegistrationView(request):	
		if request.method == 'POST':
			body_unicode = request.body.decode('utf-8')
			body = json.loads(body_unicode)

			username = body['username']
			temp_username = User.objects.filter(username= username).first()
			if temp_username is not None:
				print('This username already exists in our database! Please try another username.')
				return JsonResponse({'result' : -1})

			password = body['password']
			user_obj=User.objects.create(username=username, password=password)
			user_obj.save()

			if user_obj is not None:
				print('Success!')
				return JsonResponse({'result' : 1})
			else:
				print('There was an error. :(')
				return JsonResponse({'result' : -1})
		else:
			print('There was an error. :(')
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
				return JsonResponse({'user_token' : base64username_string})
			else:
				print('Wrong password entered!')
				return JsonResponse({'user_token' : -1})
		else:
			print('No such user in database.')
			return JsonResponse({'user_token' : -1})
	else:
		return JsonResponse({'user_token' : -1})