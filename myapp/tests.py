from django.test import TestCase
from .models import User, Follow, Tweet
import json

import os

os.system("curl -X POST http://127.0.0.1:8000/myapp/register/ -d '{\"email\":\"yourmail@gmail.com\", \"username\":\"anushree\", \"password\":\"anushree\"}' -H \"Content-Type:application/json\"")

os.system("curl -X POST http://127.0.0.1:8000/myapp/login/ -d '{\"username\": \"anushree\", \"password\":\"anushree\"}' -H \"Content-Type:application/json\"")

os.system("curl -X POST http://127.0.0.1:8000/myapp/follow/ -d '{\"follower\": \"bmlkaGk=\", \"followee\":\"c2Ft\"}' -H \"Content-Type:application/json\"")

os.system("curl -X POST http://127.0.0.1:8000/myapp/unfollow/ -d '{\"follower\": \"bmlkaGk=\", \"followee\":\"c2Ft\"}' -H \"Content-Type:application/json\"")

os.system("curl -X POST http://127.0.0.1:8000/myapp/createtweet/ -d '{\"username\": \"YW51c2g=\", \"content\":\"My first tweet!\"}' -H \"Content-Type:application/json\"")

os.system("curl -X POST http://127.0.0.1:8000/myapp/deletetweet/ -d '{\"tweet_id\": \"1\"}' -H \"Content-Type:application/json\"")

os.system("curl -X POST http://127.0.0.1:8000/myapp/readtweets/ -d '{\"username\": \"bmlkaGk=\"}' -H \"Content-Type:application/json\"")

os.system("curl -X POST http://127.0.0.1:8000/myapp/likeunlike/ -d '{\"tweet_id\": \"6\", \"activity_id\":\"1\"}' -H \"Content-Type:application/json\"")

os.system("curl -X POST http://127.0.0.1:8000/myapp/retweet/ -d '{\"tweet_id\": \"6\",\"username\":\"c2Ft\"}' -H \"Content-Type:application/json\"")
