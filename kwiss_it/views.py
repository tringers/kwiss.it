from django.http import HttpResponse
from django.shortcuts import render

def index(request):
	return HttpResponse("Hello World")

def hello_name(request, name):
	return HttpResponse("Hello {}!".format(name))