from .helper import *


def index(request):
	check_user_last_seen(request)
	return render(request, 'kwiss_it/index.html')


def datenschutz(request):
	return render(request, 'kwiss_it/datenschutz.html')


def impressum(request):
	return render(request, 'kwiss_it/impressum.html')


def settings(request):
	return render(request, 'kwiss_it/settings.html')


@require_nonlazy_user
def review(request):
	return render(request, 'kwiss_it/review.html')
