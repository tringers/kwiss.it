from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


def index(request):
	return render(request, 'kwiss_it/index.html')


def datenschutz(request):
	return render(request, 'kwiss_it/datenschutz.html')


def impressum(request):
	return render(request, 'kwiss_it/impressum.html')
