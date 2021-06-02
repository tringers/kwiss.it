import base64
import re
import string
import uuid
from datetime import datetime
from urllib.parse import unquote
import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
# noinspection PyPackageRequirements
from ratelimit.decorators import ratelimit

from .models import UserPrivate, UserPicture, UserDescription, Picture, UserLastSeen, Lobby, LobbyType, LobbyPlayer

forbidden_usernames = [
	'user',
	'username',
	'admin',
	'administrator',
	'mod',
	'moderator',
	'test',
]

allow_chars_for_email = r'^[a-z0-9.!#$%&\'*+-/=?^_`{|}~@]+$'


def check_valid_chars(inputStr: str) -> bool:
	if not re.match("^[A-Za-z0-9 _!§$%&/()=?+#*'~,.;:-]*$", inputStr):
		return False
	return True


def generate_lobby_key():
	key_int = random.randint(pow(16, 5), pow(16, 6) - 1)
	key = '{0:06x}'.format(key_int).upper()
	return key


def check_user_last_seen(request):
	##TODO guest
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
		inputEmail = request.POST.get('inputEmail')
		inputUsername = request.POST.get('inputUsername')
		inputName = request.POST.get('inputName')
		inputPassword = request.POST.get('inputPassword')
		inputPassword2 = request.POST.get('inputPassword2')
		##TODO guest
		if request.user.is_authenticated:
			args['errorMsg'] = 'Bereits angemeldet.'
			return register_end(request, args)

		# Check if everything was entered
		if not buttonRegister or not inputEmail or not inputUsername or not inputName or not inputPassword or not inputPassword2:
			args['errorMsg'] = 'One of the required values were not present'
			return register_end(request, args)

		# Set email and username lower
		inputEmail = inputEmail.lower()
		inputUsername = inputUsername.lower()
		if not check_valid_chars(inputEmail):
			return 'Email beinhaltet nicht valide Zeichen.'
		if not check_valid_chars(inputName):
			return 'Anzeigename beinhaltet nicht valide Zeichen.'
		if not check_valid_chars(inputPassword):
			return 'Passwort beinhaltet nicht valide Zeichen.'
		if not check_valid_chars(inputPassword2):
			return 'Passwort2 beinhaltet nicht valide Zeichen.'
		if not check_valid_chars(inputUsername):
			return 'Benutzername beinhaltet nicht valide Zeichen.'
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
		if len(inputName) < 4:
			args['errorMsg'] = 'Anzeigename zu kurz, Mindestlänge beträgt 4 Zeichen.'
			return register_end(request, args)
		if len(inputName) > 64:
			args['errorMsg'] = 'Anzeigename zu lang, maximal 64 Zeichen erlaubt.'
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

		if not re.compile(allow_chars_for_email).search(inputEmail):
			args['errorMsg'] = 'Bitte valide Email Adresse eingeben.'
			return register_end(request, args)

		# Check if username only contains letter, digits, underscore or minus
		if not re.match("^[A-Za-z0-9_-]*$", inputUsername):
			args['errorMsg'] = 'Benutzername enthält ungültige Zeigen'
			return register_end(request, args)

		# Check if display name only contains valid characters
		# TODO: Selben Check auch beim Abändern nutzen
		if not re.match("^[A-Za-z0-9 _!§$%&/()=?+#*'~,.;:-]*$", inputName):
			args['errorMsg'] = 'Anzeigename enthält ungültige Zeigen'
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
		user_obj.first_name = inputName
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
	if not check_valid_chars(username):
		return register_checkusername_res(403, 'Benutzername "' + username + '" ist nicht erlaubt.')
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
	##TODO guest
	if request.user.is_authenticated:
		return redirect('/user/' + request.user.username)
	else:
		return redirect('index')


def user_profile(request, username):
	check_user_last_seen(request)
	args = {
		'infoMsg': '',
		'errorMsg': '',
		'errorCode': 0,
		'userprofile': {
			'requested': username,
			'username': '',
			'firstname': '',
			'private': False,
			'picture': '',
			'description': '',
			'registered': '',
			'lastseen': '',
			'registeredDisable': False,
			'lastseenDisable': False,
		},
	}

	if request.method == 'POST':
		args['errorMsg'] = user_profile_post(request)
		if args['errorMsg'] == '':
			args['infoMsg'] = 'Erfolgreich gespeichert.'

	username = username.lower()

	# User Object
	profileAS = User.objects.filter(username=username)
	if len(profileAS) < 1:
		args['errorMsg'] = 'Kein Benutzer mit dem Benutzernamen gefunden.'
		args['errorCode'] = 1
		return render(request, 'kwiss_it/user.html', args)
	profileA = profileAS[0]

	profileBS = UserPicture.objects.filter(Uid=profileA.id)
	profileCS = UserDescription.objects.filter(Uid=profileA.id)
	profileDS = UserPrivate.objects.filter(Uid=profileA.id)
	userprofile = args['userprofile']

	userprofile['requested'] = profileA.first_name
	userprofile['username'] = profileA.first_name
	userprofile['firstname'] = profileA.first_name
	userprofile['username'] = profileA.username
	userprofile['registered'] = profileA.date_joined.strftime("%Y-%m-%d")
	uls_objset = UserLastSeen.objects.filter(Uid=profileA.id)
	if len(uls_objset) > 0:
		uls_obj = uls_objset[0]
		userprofile['lastseen'] = uls_obj.LastSeen.strftime("%Y-%m-%d %H:%M")

	# Check for profile private
	if len(profileDS) > 0:
		profileD = profileDS[0]
		userprofile['private'] = profileD.UPprivate
		userprofile['registeredDisable'] = profileD.UPregistered
		userprofile['lastseenDisable'] = profileD.UPlastseen

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
		description = base64.b64decode(profileC.Udescription.encode(encoding='utf-8')).decode(encoding='utf-8')
		userprofile['description'] = description

	args['userprofile'] = userprofile
	return render(request, 'kwiss_it/user.html', args)


def user_profile_post(request):
	# Detect, which changes should be done
	# - User Picture
	# - User Display Name
	# - User Description
	# - Email Address
	# - User Password
	##TODO guest
	if not request.user.is_authenticated:
		return 'Benutzer nicht angemeldet. Ungültige Aktion'

	buttonDescription = request.POST.get('inputChangeProfile')
	buttonPassword = request.POST.get('inputChangePassword')
	html = r'(<([a-zA-Z \/!])+([^>])*)'
	errorMsg = ''

	if buttonDescription:
		inputName = request.POST.get('inputName')
		inputDescription = request.POST.get('newDescription')
		inputProfilePrivate = request.POST.get('checkProfilePrivate')
		inputRegistered = request.POST.get('checkRegistered')
		inputLastSeen = request.POST.get('checkLastSeen')
		if not check_valid_chars(inputName):
			return 'Benutzernamen beinhaltet nicht valide Zeichen.'

		modelsetUser = User.objects.filter(username=request.user.username)
		inputDescription = re.compile(html).sub('', inputDescription)
		inputDescription = base64.b64encode(inputDescription.encode(encoding='utf-8')).decode(encoding='utf-8')

		if len(modelsetUser) < 1:
			return 'Kein Benutzer mit dem Benutzernamen gefunden.'
		modelUser = modelsetUser[0]

		modelsetDescription = UserDescription.objects.filter(Uid=modelUser.id)
		modelsetPrivacy = UserPrivate.objects.filter(Uid=modelUser.id)

		# Check if model entries exist
		# Else create
		if len(modelsetDescription) > 0:
			modelDescription = modelsetDescription[0]
		else:
			# Create Description
			modelDescription = UserDescription.objects.create(Uid=modelUser, Udescription='')
			modelDescription.save()

		if len(modelsetPrivacy) > 0:
			modelPrivacy = modelsetPrivacy[0]
		else:
			# Create Description
			modelPrivacy = UserPrivate.objects.create(Uid=modelUser)
			modelPrivacy.save()

		# Set information
		modelUser.first_name = inputName
		modelUser.save()

		modelDescription.Udescription = inputDescription
		modelDescription.save()

		modelPrivacy.UPprivate = inputProfilePrivate is not None
		modelPrivacy.UPregistered = inputRegistered is None
		modelPrivacy.UPlastseen = inputLastSeen is None
		modelPrivacy.save()
	elif buttonPassword:
		pass

	return errorMsg


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
		if not check_valid_chars(inputPassword):
			args["errorMsg"] = "Passwort beinhaltet nicht valide Zeichen"
			return render(request, 'kwiss_it/login.html', args)
		if not check_valid_chars(inputUsername):
			args["errorMsg"] = "Benutzernamen beinhaltet nicht valide Zeichen"
			return render(request, 'kwiss_it/login.html', args)
		##TODO guest
		if request.user.is_authenticated:
			args['errorMsg'] = 'Bereits angemeldet.'
			return render(request, 'kwiss_it/login.html', args)

		if not buttonLogin or not inputUsername or not inputPassword:
			args['errorMsg'] = 'Login fehlgeschlagen. Nicht alle notwendigen Daten wurden eingegeben.'
			return render(request, 'kwiss_it/index.html', args)

		user_obj = authenticate(request, username=inputUsername.lower(), password=inputPassword)

		if user_obj is not None:
			# Redirect to a success page.
			login(request, user_obj)
			args['infoMsg'] = 'Login erfolgreich.'
			pass
		else:
			# Return an 'invalid login' error message.
			args['errorMsg'] = 'Login fehlgeschlagen.'
			pass

	return render(request, 'kwiss_it/index.html', args)


def logout_view(request):
	args = {}

	logout(request)
	args['infoMsg'] = 'Erfolgreich abgemeldet.'

	return render(request, 'kwiss_it/logout.html', args)


def review(request):
	return render(request, 'kwiss_it/review.html')


@ratelimit(key='ip', rate='6/m', method='POST')
def createlobby_view(request):
	args = {
		'errorMsg': '',
		'infoMsg': ''
	}

	if request.method == 'POST':
		lobby_create: str = request.POST.get('buttoncreate')
		lobby_name: str = request.POST.get('createlobbyname')
		question_amount: str = request.POST.get('questionamountfield')
		lobby_type: str = request.POST.get('lobbytype')
		game_mode: str = request.POST.get('gamemode')
		inputPassword: str = request.POST.get('lobbypassword')
		time_amount: str = request.POST.get('timeamountfield')
		player_amount: str = request.POST.get('playeramountfield')

		if not time_amount.isnumeric():
			args['errorMsg'] = 'Zeit muss eine Nummer sein'
			return createlobby_end(request, args)
		time_amount = int(time_amount)

		if not player_amount.isnumeric():
			args['errorMsg'] = 'Spielermenge muss eine Nummer sein'
			return createlobby_end(request, args)
		player_amount = int(player_amount)

		if not question_amount.isnumeric():
			args['errorMsg'] = 'Fragemenge muss eine Nummer sein'
			return createlobby_end(request, args)
		question_amount = int(question_amount)
		##TODO guest
		if not request.user.is_authenticated:
			args['errorMsg'] = 'User muss angemeldet sein um eine Lobby erstellen zu können'
			return createlobby_end(request, args)

		if not lobby_create or not game_mode or not lobby_type or not question_amount or not time_amount or not lobby_type or not player_amount:
			args['errorMsg'] = 'Eine der erforderlichen Felder wurde nicht ausgefüllt'
			return createlobby_end(request, args)

		if not lobby_name:
			lobby_name = f"{request.user.username}'s Raum"
		else:
			if not check_valid_chars(lobby_name):
				args['errorMsg'] = 'Lobbyname enthält ungültige Zeigen'
				createlobby_end(request, args)
		if question_amount < 1 or question_amount > 64:
			args['errorMsg'] = 'ungültige Fragenmenge'
			return createlobby_end(request, args)
		if player_amount < 2 or player_amount > 16:
			args['errorMsg'] = 'ungültige Spielermenge'
			return createlobby_end(request, args)

		if lobby_type != "Öffentlich" and lobby_type != "Privat":
			args['errorMsg'] = 'ungültiger Lobbytyp'
			return createlobby_end(request, args)
		if inputPassword is not None and inputPassword != "":
			if not check_valid_chars(inputPassword):
				args['errorMsg'] = 'Passwort enthält ungültige Zeigen'
				return createlobby_end(request, args)
		else:
			inputPassword = None

		game_mode_objset = LobbyType.objects.filter(LTname=game_mode)
		if len(game_mode_objset) < 1:
			args['errorMsg'] = 'ungültiger Spielemodus'
			return createlobby_end(request, args)

		uuid_token = uuid.uuid4()
		unique = True
		lobby_key = ""
		counter = 0
		while (unique):
			lobby_key = generate_lobby_key()
			if len(Lobby.objects.filter(Lkey=lobby_key)) == 0:
				unique = False
			else:
				counter += 1
				if counter >= 50:
					args[
						"errorMsg"] = 'Es ist ein Fehler beim Lobbyerstellen aufgetreten bitte in wenigen Minuten erneut Probieren.'
					return createlobby_end(request, args)
		lobby_obj = Lobby.objects.create(Uid=request.user, Lname=lobby_name, Ltype=game_mode_objset[0],
		                                 Lplayerlimit=player_amount,Lpassword=inputPassword,Lauthtoken=uuid_token,
		                                 Lkey=lobby_key)
		lobby_obj.save()
		return redirect(f'/lobby/{lobby_obj.Lkey}/{uuid_token}/')

	return render(request, 'kwiss_it/createlobby.html', args)


def createlobby_end(request, args):
	if args is None or not args:
		args = {
			'errorMsg': '',
			'infoMsg': ''
		}
	return render(request, 'kwiss_it/createlobby.html', args)


def lobbylist_view(request):
	args = {
		'errorMsg': '',
		'infoMsg': ''
	}
	return render(request, 'kwiss_it/lobbylist.html', args)


def join_lobby(Lkey, user_obj: User, password=None, authtoken=None):
	lobby_set = Lobby.objects.filter(Lkey=Lkey)
	if len(lobby_set) != 1:
		return [False, 'Lobby konnte nicht gefunden werden']
	LP_objset = LobbyPlayer.objects.filter(Uid=user_obj)
	if len(LP_objset) > 0:
		return [False, 'Spieler bereits in einer Lobby']
	lobby = lobby_set[0]
	test_valid = False
	player_amount = len(LobbyPlayer.objects.filter(Lid=lobby))
	if lobby.Lpassword is None and not player_amount >= lobby.Lplayerlimit:
		test_valid = True
	elif lobby.Lpassword is not None and lobby.Lpassword == password and player_amount >= lobby.Lplayerlimit:
		test_valid = True
	elif lobby.Lauthtoken is not None and lobby.Lauthtoken == authtoken and player_amount >= lobby.Lplayerlimit:
		test_valid = True
	if test_valid:
		LPobj=LobbyPlayer.objects.create(Lid=lobby, Uid=user_obj)
		LPobj.save()
		return [True, 'Lobby erfolgreich beigetreten']
	else:
		return [False, 'Lobby konnte nicht beigetreten werden']


def lobby_view(request, lobby_key, auth_token=None):
	args = {
		'errorMsg': '',
		'infoMsg': '',
	}
	request.GET.get('')
	result = join_lobby(lobby_key, request.user, None, auth_token)
	if result[0]:
		args['auth_token'] = auth_token
		args['lobby_key'] = lobby_key
		return render(request, 'kwiss_it/lobby.html', args)
	else:
		args['errorMsg'] = result[1]
		return render(request, 'kwiss_it/lobbylist.html', args)
