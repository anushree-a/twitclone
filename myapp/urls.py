from django.urls import path
from . import views

urlpatterns = [
	path('register/', views.RegistrationView, name='RegistrationView'),
	path('login/', views.LoginView, name='LoginView'),
	path('activate/', views.ActivationView, name='ActivationView'),
    path('', views.index, name='index'),
]