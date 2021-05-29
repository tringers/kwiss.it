import string
import pytz
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.models import User
from .models import UserPicture, UserDescription, Picture, UserLastSeen
from django.contrib.auth import authenticate, login, logout
# noinspection PyPackageRequirements
from ratelimit.decorators import ratelimit
from urllib.parse import unquote


forbidden_usernames = [
	'user',
	'username',
	'admin',
	'administrator',
	'mod',
	'moderator',
	'test',
]


def check_user_last_seen(request):
	if not request.user.is_authenticated:
		return

	username = request.user.username
	user_objset = User.objects.filter(username=username)

	if len(user_objset) < 1:
		return

	user_obj = user_objset[0]

	uls_objset = UserLastSeen.objects.filter(Uid=user_obj)

	if len(uls_objset) < 1:
		uls_obj = UserLastSeen.objects.create(Uid=user_obj)
		uls_obj.save()
		pass
	else:
		uls_obj = uls_objset[0]
		uls_obj.LastSeen = datetime.now()

	return


def index(request):
	check_user_last_seen(request)
	return render(request, 'kwiss_it/index.html')


def datenschutz(request):
	return render(request, 'kwiss_it/datenschutz.html')


def impressum(request):
	return render(request, 'kwiss_it/impressum.html')


def lobby(request, lobby_id):
	check_user_last_seen(request)
	return render(request, 'kwiss_it/lobby.html')


def settings(request):
	return render(request, 'kwiss_it/settings.html')


@ratelimit(key='ip', rate='6/m', method='POST')
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

		# Check if username is allowed
		if any(inputUsername.lower() in s for s in forbidden_usernames):
			args['errorMsg'] = 'Benutzername nicht erlaubt.'
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

		user_obj = User.objects.create_user(inputUsername, inputEmail, inputPassword)
		# TODO: Send mail to user
		# TODO: After email validation: Set is_active to 1
		# TODO: After email validation: Create all necessary model entries
		user_obj.is_active = 0
		user_obj.save()
		args['infoMsg'] = 'Bestätige deine Email Adresse, danach kannst du dich anmelden.'
		return register_end(request, args)

	return register_end(request, args)


def register_end(request, args=None):
	if args is None or not args:
		args = {
			'errorMsg': '',
			'infoMsg': ''
		}

	return render(request, 'kwiss_it/register.html', args)


# Burst limit and normal limit
@ratelimit(key='ip', rate='30/m', method='ALL')
@ratelimit(key='ip', rate='60/h', method='ALL')
def register_checkusername(request, username):
	# If user found, status 409 with appropriate msg
	username = unquote(username)
	user_objset = User.objects.filter(username=username)

	if any(username.lower() in f for f in forbidden_usernames):
		return register_checkusername_res(403, 'Benutzername "' + username + '" ist nicht erlaubt.')

	if len(user_objset) > 0:
		return register_checkusername_res(409, 'Benutzername "' + username + '" ist bereits vergeben.')

	return register_checkusername_res(200, '')


def register_checkusername_short(request):
	return register_checkusername_res(200, '')


def register_checkusername_res(status, msg):
	return JsonResponse({
		'status': status,
		'message': msg,
	})


def user_short(request, username):
	return redirect('/user/' + username)


def user(request):
	if request.user.is_authenticated:
		return redirect('/user/' + request.user.username)
	else:
		return redirect('index')


def user_profile(request, username):
	check_user_last_seen(request)
	args = {
		'infoMsg': '',
		'errorMsg': '',
		'userprofile': {
			'requested': username,
			'username': '',
			'picture': '',
			'description': '',
			'registered': '',
			'lastseen': '',
		},
	}

	if request.method == 'POST':
		args['errorMsg'] = user_profile_post(request)
		if args['errorMsg'] == '':
			args['infoMsg'] = 'Erfolgreich gespeichert.'

	# User Object
	profileAS = User.objects.filter(username=username)
	if len(profileAS) < 1:
		args['errorMsg'] = 'Kein Benutzer mit dem Benutzernamen gefunden.'
		return render(request, 'kwiss_it/user.html', args)
	profileA = profileAS[0]

	profileBS = UserPicture.objects.filter(Uid=profileA.id)
	profileCS = UserDescription.objects.filter(Uid=profileA.id)
	userprofile = args['userprofile']

	userprofile['username'] = profileA.username
	userprofile['registered'] = profileA.date_joined.strftime("%Y-%m-%d")
	uls_objset = UserLastSeen.objects.filter(Uid=profileA.id)
	if len(uls_objset) > 0:
		uls_obj = uls_objset[0]
		userprofile['lastseen'] = uls_obj.LastSeen.strftime("%Y-%m-%d %H:%M")

	# Profile Picture
	if len(profileBS) > 0:
		profileB = profileBS[0]
		profilePS = Picture.objects.get(id=profileB.Pid)
		if len(profilePS) > 0:
			profileP = profilePS[0]
			userprofile['picture'] = profileP.Pcontent

	# User description
	if len(profileCS) > 0:
		profileC = profileCS[0]
		userprofile['description'] = profileC.Udescription

	args['userprofile'] = userprofile

	return render(request, 'kwiss_it/user.html', args)


def user_profile_post(request):
	# Detect, which changes should be done
	# - User Picture
	# - User Description
	# - Email Address
	# - User Password
	return ''


@ratelimit(key='ip', rate='6/m', method='POST')
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
