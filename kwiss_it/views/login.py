from .helper import *


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
		inputStayloggedin = request.POST.get('stayloggedin')
		if not check_valid_chars(inputPassword):
			args["errorMsg"] = "Passwort beinhaltet nicht valide Zeichen"
			return render(request, 'kwiss_it/login.html', args)
		if not check_valid_chars(inputUsername):
			args["errorMsg"] = "Benutzernamen beinhaltet nicht valide Zeichen"
			return render(request, 'kwiss_it/login.html', args)

		if request.user.is_authenticated:
			args['errorMsg'] = 'Bereits angemeldet.'
			return render(request, 'kwiss_it/login.html', args)

		if is_lazy_user(request.user):
			args['errorMsg'] = 'Mit temporärem Benutzer angemeldet. Bitte registrieren.'
			return render(request, 'kwiss_it/login.html', args)

		if not buttonLogin or not inputUsername or not inputPassword:
			args['errorMsg'] = 'Login fehlgeschlagen. Nicht alle notwendigen Daten wurden eingegeben.'
			return render(request, 'kwiss_it/index.html', args)

		user_obj = authenticate(request, username=inputUsername.lower(), password=inputPassword)

		if user_obj is not None:
			# Set session expire
			if inputStayloggedin is not None:
				request.session.set_expiry(None)
			else:
				request.session.set_expiry(0)

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
