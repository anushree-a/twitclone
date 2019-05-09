from django.test import TestCase
from .models import User, Follow, Tweet
import os

#Automated the curl commands to test out the project's functionalities.

# os.system("curl -X POST http://127.0.0.1:8000/myapp/register/ -d '{\"email\":\"yourmail@gmail.com\", \"username\":\"anushree\", \"password\":\"anushree\"}' -H \"Content-Type:application/json\"")

# os.system("curl -X POST http://127.0.0.1:8000/myapp/login/ -d '{\"username\": \"anushree\", \"password\":\"anushree\"}' -H \"Content-Type:application/json\"")

# os.system("curl -X POST http://127.0.0.1:8000/myapp/follow/ -d '{\"follower\": \"bmlkaGk=\", \"followee\":\"c2Ft\"}' -H \"Content-Type:application/json\"")

# os.system("curl -X POST http://127.0.0.1:8000/myapp/unfollow/ -d '{\"follower\": \"bmlkaGk=\", \"followee\":\"c2Ft\"}' -H \"Content-Type:application/json\"")

# os.system("curl -X POST http://127.0.0.1:8000/myapp/createtweet/ -d '{\"username\": \"c2Ft\", \"content\":\"My first tweet!\"}' -H \"Content-Type:application/json\"")

# os.system("curl -X POST http://127.0.0.1:8000/myapp/deletetweet/ -d '{\"tweet_id\": \"1\"}' -H \"Content-Type:application/json\"")

# os.system("curl -X POST http://127.0.0.1:8000/myapp/readtweets/ -d '{\"username\": \"bmlkaGk=\"}' -H \"Content-Type:application/json\"")

# os.system("curl -X POST http://127.0.0.1:8000/myapp/likeunlike/ -d '{\"tweet_id\": \"24\", \"activity_id\":\"1\"}' -H \"Content-Type:application/json\"")

# os.system("curl -X POST http://127.0.0.1:8000/myapp/retweet/ -d '{\"tweet_id\": \"24\",\"username\":\"c2Ft\"}' -H \"Content-Type:application/json\"")


import json
import requests
from django_test_curl import CurlClient


class SimpleTest(TestCase):
	def setUp(self):
		self.client = CurlClient()

	def test_details(self):
		print('Creating accounts......')
		response = self.client.curl("""curl http://127.0.0.1:8000/myapp/register/ -d '{"email":"mail@gmail.com", "username":"anushree", "password":"anushree"}' -H "Content-Type:application/json" """)
		self.assertEqual(response.status_code, 200)

		print('Activating accounts......')
		temp_user = User.objects.filter(username="anushree").first()
		temp_user.isactive = True;
		print(temp_user.username, 'activated.')
		temp_user.save()

		print('Logging in......')
		response = self.client.curl("""curl http://127.0.0.1:8000/myapp/login/ -d '{"username": "anushree", "password":"anushree"}' -H "Content-Type:application/json" """)
		self.assertEqual(response.status_code, 200)		

		print('Creating and activating 2 more accounts......')
		response = self.client.curl("""curl http://127.0.0.1:8000/myapp/register/ -d '{"email":"mail@gmail.com", "username":"sam", "password":"sam"}' -H "Content-Type:application/json" """)
		response = self.client.curl("""curl http://127.0.0.1:8000/myapp/register/ -d '{"email":"mail@gmail.com", "username":"nidhi", "password":"nidhi"}' -H "Content-Type:application/json" """)
		temp_user = User.objects.filter(username="sam").first()
		temp_user.isactive = True;
		print(temp_user.username, 'activated.')
		temp_user.save()
		temp_user = User.objects.filter(username="nidhi").first()
		temp_user.isactive = True;
		print(temp_user.username, 'activated.')
		temp_user.save()

		print('Follow.....')
		response = self.client.curl(""" curl http://127.0.0.1:8000/myapp/follow/ -d '{"follower": "bmlkaGk=", "followee":"c2Ft"}' -H "Content-Type:application/json" """)
		self.assertEqual(response.status_code, 200)

		print('Unfollow.....')
		response = self.client.curl(""" curl http://127.0.0.1:8000/myapp/unfollow/ -d '{"follower": "bmlkaGk=", "followee":"c2Ft"}' -H "Content-Type:application/json" """)
		self.assertEqual(response.status_code, 200)

		print('Create tweet.....')
		response = self.client.curl(""" curl http://127.0.0.1:8000/myapp/createtweet/ -d '{"username": "bmlkaGk=", "content":"My first tweet!"}' -H "Content-Type:application/json" """)
		response = self.client.curl(""" curl http://127.0.0.1:8000/myapp/createtweet/ -d '{"username": "bmlkaGk=", "content":"My second tweet!"}' -H "Content-Type:application/json" """)
		self.assertEqual(response.status_code, 200)

		print('Delete tweet.....')
		response = self.client.curl(""" curl http://127.0.0.1:8000/myapp/deletetweet/ -d '{"tweet_id":"1"}' -H "Content-Type:application/json" """)
		self.assertEqual(response.status_code, 200)

		print('Read tweets......')
		response = self.client.curl(""" curl http://127.0.0.1:8000/myapp/readtweets/ -d '{"username":"bmlkaGk="}' -H "Content-Type:application/json" """)
		self.assertEqual(response.status_code, 200)

		print('Liking tweet......')
		response = self.client.curl(""" curl http://127.0.0.1:8000/myapp/likeunlike/ -d '{"tweet_id":"2", "activity_id":"1"}' -H "Content-Type:application/json" """)
		self.assertEqual(response.status_code, 200)

		print('Retweeting......')
		response = self.client.curl(""" curl http://127.0.0.1:8000/myapp/retweet/ -d '{"tweet_id": "2","username":"c2Ft"}' -H "Content-Type:application/json" """)
		self.assertEqual(response.status_code, 200)

		print('Replying to tweet......')
		response = self.client.curl(""" curl http://127.0.0.1:8000/myapp/replytweet/ -d '{"tweet_id": "2","username":"bmlkaGk=", "reply_content":"Nice!"}' -H "Content-Type:application/json" """)
		self.assertEqual(response.status_code, 200)