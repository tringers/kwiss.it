from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


def index(request):
	return HttpResponse("Hello World")

def template(request):
	return render(request, 'kwiss_it/index.html')
