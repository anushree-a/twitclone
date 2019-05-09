from django.contrib import admin
from .models import User, Follow, Tweet, TweetActivity, TweetReply

admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Tweet)
admin.site.register(TweetActivity)
admin.site.register(TweetReply)
