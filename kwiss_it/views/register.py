from .helper import *


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

		if request.user.is_authenticated:
			args['errorMsg'] = 'Bereits angemeldet.'
			return register_end(request, args)

		if is_lazy_user(request.user):
			args['errorMsg'] = 'Mit temporärem Benutzer angemeldet. Bitte nochmal auf Registrieren klicken.'
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
