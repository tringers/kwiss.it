import string
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


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
	args = {
		'errorMsg': '',
		'infoMsg': ''
	}

	if request.method == 'POST':
		buttonRegister = request.POST.get('buttonRegister')
		inputEmail = request.POST.get('inputEmail').lower()
		inputUsername = request.POST.get('inputUsername')
		inputPassword = request.POST.get('inputPassword')
		inputPassword2 = request.POST.get('inputPassword2')

		if request.user.is_authenticated:
			args['errorMsg'] = 'Bereits angemeldet.'
			return register_end(request, args)

		# Check if everything was entered
		if not buttonRegister or not inputEmail or not inputUsername or not inputPassword or not inputPassword2:
			args['errorMsg'] = 'One of the required values were not present'
			return register_end(request, args)

		# Check min max length of username, email address and password
		if len(inputEmail) < 6 or len(inputEmail) > 320:
			args['errorMsg'] = 'Bitte valide Email Adresse angeben.'
			return register_end(request, args)

		if len(inputUsername) < 4:
			args['errorMsg'] = 'Benutzername zu kurz, Mindestlänge beträgt 4 Zeichen.'
			return register_end(request, args)
		if len(inputUsername) > 64:
			args['errorMsg'] = 'Benutzername zu lang, maximal 64 Zeichen erlaubt.'
			return register_end(request, args)
		if len(inputPassword) < 8:
			args['errorMsg'] = 'Password zu kurz, Mindestlänge beträgt 8 Zeichen.'
			return register_end(request, args)
		if len(inputPassword) > 64:
			args['errorMsg'] = 'Password zu lang, maximal 64 Zeichen erlaubt.'
			return register_end(request, args)

		# Check if username or email address exists
		try:
			User.objects.get(email=inputEmail)
			args['errorMsg'] = 'Email Adresse bereits in Verwendung.'
			return register_end(request, args)
		except User.DoesNotExist:
			pass

		try:
			User.objects.get(username=inputUsername)
			args['errorMsg'] = 'Benutzername bereits in Verwendung.'
			return register_end(request, args)
		except User.DoesNotExist:
			pass

		# check if email is email-shaped
		inputEmailcount = inputEmail.count('@')
		if inputEmailcount == 0 or inputEmailcount > 1:
			args['errorMsg'] = 'Bitte valide Email Adresse eingeben.'
			return register_end(request, args)

		# Check if password meets requirements
		if inputPassword != inputPassword2:
			args['errorMsg'] = 'Passwörter sind nicht identisch.'
			return register_end(request, args)

		strength = 0

		# Check for digit char
		if any(char.isdigit() for char in inputPassword):
			strength += 1

		# Check for lowercase char
		if any(char.islower() for char in inputPassword):
			strength += 1

		# Check for uppercase char
		if any(char.isupper() for char in inputPassword):
			strength += 1

		# Check for special char
		punctuation_set = set(string.punctuation)
		if set(inputPassword).intersection(punctuation_set):
			strength += 1

		if strength < 3:
			args['errorMsg'] = 'Password erfüllt nicht die Mindestvoraussetzungen.'
			return register_end(request, args)

		# TODO: Register user / Check the following code
		user_obj = User.objects.create_user(inputUsername, inputEmail, inputPassword)
		user_obj.save()
		args['infoMsg'] = 'Registrierung erfolgreich, bitte anmelden.'
		return register_end(request, args)

	return register_end(request, args)


def register_end(request, args=None):
	if args is None or not args:
		args = {
			'errorMsg': '',
			'infoMsg': ''
		}

	return render(request, 'kwiss_it/register.html', args)


def user(request):
	return render(request, 'kwiss_it/user.html')


def login_view(request, args=None):
	if args is None or not args:
		args = {
			'errorMsg': '',
			'infoMsg': ''
		}

	if request.method == 'POST':
		buttonLogin = request.POST.get('buttonLogin')
		inputUsername = request.POST.get('inputUsername')
		inputPassword = request.POST.get('inputPassword')

		if request.user.is_authenticated:
			args['errorMsg'] = 'Bereits angemeldet.'
			return render(request, 'kwiss_it/login.html', args)

		if not buttonLogin or not inputUsername or not inputPassword:
			args['errorMsg'] = 'One of the required values were not present.'
			return register_end(request, args)

		user_obj = authenticate(request, username=inputUsername, password=inputPassword)

		if user_obj is not None:
			# Redirect to a success page.
			login(request, user_obj)
			args['infoMsg'] = 'Login erfolgreich.'
			pass
		else:
			# Return an 'invalid login' error message.
			args['errorMsg'] = 'Login fehlgeschlagen.'
			pass

	return render(request, 'kwiss_it/login.html', args)


def logout_view(request):
	args = {}

	logout(request)
	args['infoMsg'] = 'Erfolgreich abgemeldet.'

	return render(request, 'kwiss_it/logout.html', args)


def review(request):
	return render(request, 'kwiss_it/review.html')
