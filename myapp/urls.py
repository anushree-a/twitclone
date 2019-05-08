from django.urls import path
from . import views

urlpatterns = [
	path('retweet/', views.RetweetView, name='RetweetView'),
	path('likeunlike/', views.LikeUnlikeView, name='LikeUnlikeView'),
	path('readtweets/', views.ReadTweets, name='ReadTweets'),
	path('deletetweet/', views.DeleteTweet, name='DeleteTweet'),
	path('createtweet/', views.CreateTweet, name='CreateTweet'),
	path('unfollow/', views.UnfollowView, name='UnfollowView'),
	path('follow/', views.FollowView, name='FollowView'),
	path('register/', views.RegistrationView, name='RegistrationView'),
	path('login/', views.LoginView, name='LoginView'),
	path('activate/<username>', views.ActivationView, name='ActivationView'),
    path('', views.index, name='index'),
]