from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


def index(request):
	return render(request, 'kwiss_it/index.html')


def datenschutz(request):
	return render(request, 'kwiss_it/datenschutz.html')


def impressum(request):
	return render(request, 'kwiss_it/impressum.html')


def lobby(request, lobby_id):
	return render(request, 'kwiss_it/lobby.html')


def settings(request):
	return render(request, 'kwiss_it/settings.html')


def register(request):
	return render(request, 'kwiss_it/register.html')


def user(request):
	return render(request, 'kwiss_it/user.html')


def login(request):
	return render(request, 'kwiss_it/login.html')


def review(request):
	return render(request, 'kwiss_it/review.html')
