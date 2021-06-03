from .helper import *


def user_short_view(request, username):
	return redirect('/user/' + username)


def user_view(request):
	if request.user.is_authenticated and not is_lazy_user(request.user):
		return redirect('/user/' + request.user.username)
	else:
		return redirect('index')


def user_profile_view(request, username):
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
	user_objset = User.objects.filter(username=username)
	if len(user_objset) < 1:
		args['errorMsg'] = 'Kein Benutzer mit dem Benutzernamen gefunden.'
		args['errorCode'] = 1
		return render(request, 'kwiss_it/user.html', args)
	user_obj = user_objset[0]

	userpicture_objset = UserPicture.objects.filter(Uid=user_obj)
	description_objset = UserDescription.objects.filter(Uid=user_obj)
	privacy_objset = UserPrivate.objects.filter(Uid=user_obj)

	userprofile = args['userprofile']

	userprofile['requested'] = user_obj.first_name
	userprofile['username'] = user_obj.first_name
	userprofile['firstname'] = user_obj.first_name
	userprofile['username'] = user_obj.username
	userprofile['registered'] = user_obj.date_joined.strftime("%Y-%m-%d")

	# Get time when user was last seen
	lastseen_objset = UserLastSeen.objects.filter(Uid=user_obj)
	if len(lastseen_objset) > 0:
		lastseen_obj = lastseen_objset[0]
		userprofile['lastseen'] = lastseen_obj.LastSeen.strftime("%Y-%m-%d %H:%M")

	# Check for profile private
	if len(privacy_objset) > 0:
		privacy_obj = privacy_objset[0]
		userprofile['private'] = privacy_obj.UPprivate
		userprofile['registeredDisable'] = privacy_obj.UPregistered
		userprofile['lastseenDisable'] = privacy_obj.UPlastseen

	# Get Profile Picture
	if len(userpicture_objset) > 0:
		userpicture_obj = userpicture_objset[0]
		picture_objset = Picture.objects.filter(id=userpicture_obj.Pid)
		if len(picture_objset) > 0:
			picture_obj = picture_objset[0]
			userprofile['picture'] = picture_obj.Pcontent

	# Get User description
	if len(description_objset) > 0:
		description_obj = description_objset[0]
		userprofile['description'] = b64decode(description_obj.Udescription)

	args['userprofile'] = userprofile
	return render(request, 'kwiss_it/user.html', args)


def user_profile_post(request):
	# Detect, which changes should be done
	# - User Picture
	# - User Display Name
	# - User Description
	# - Email Address
	# - User Password
	if not request.user.is_authenticated:
		return 'Benutzer nicht angemeldet. Ungültige Aktion.'

	if is_lazy_user(request.user):
		return 'Dies ist nur ein temporärer User, bitte registriere dich erst.'

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

		user_objset = User.objects.filter(username=request.user.username)
		inputDescription = re.compile(html).sub('', inputDescription)
		inputDescription = b64encode(inputDescription)

		if len(user_objset) < 1:
			return 'Kein Benutzer mit dem Benutzernamen gefunden.'
		user_obj = user_objset[0]

		description_objset = UserDescription.objects.filter(Uid=user_obj)
		privacy_objset = UserPrivate.objects.filter(Uid=user_obj)

		# Check if model entries exist
		# Else create
		if len(description_objset) > 0:
			description_obj = description_objset[0]
		else:
			# Create Description
			description_obj = UserDescription.objects.create(Uid=user_obj, Udescription='')
			description_obj.save()

		if len(privacy_objset) > 0:
			privacy_obj = privacy_objset[0]
		else:
			# Create Description
			privacy_obj = UserPrivate.objects.create(Uid=user_obj)
			privacy_obj.save()

		# Set information
		user_obj.first_name = inputName
		user_obj.save()

		description_obj.Udescription = inputDescription
		description_obj.save()

		privacy_obj.UPprivate = inputProfilePrivate is not None
		privacy_obj.UPregistered = inputRegistered is None
		privacy_obj.UPlastseen = inputLastSeen is None
		privacy_obj.save()
	elif buttonPassword:
		# TODO: Implement change-password form functionality
		pass

	return errorMsg
