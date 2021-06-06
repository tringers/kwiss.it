from .helper import *


def lobbylist_view(request):
	check_old_heartbeat()
	check_old_lobbys()
	args = {
		'errorMsg': '',
		'infoMsg': ''
	}

	return render(request, 'kwiss_it/lobbylist.html', args)


@ratelimit(key='ip', rate='6/m', method='POST')
def createlobby_view(request):
	check_old_heartbeat()
	args = {
		'errorMsg': '',
		'infoMsg': ''
	}

	if request.method != 'POST':
		return render(request, 'kwiss_it/createlobby.html', args)

	inputLobbycreate: str = request.POST.get('buttoncreate')
	inputLobbyname: str = request.POST.get('createlobbyname')
	inputLobbytype: str = request.POST.get('lobbytype')
	inputGamemode: str = request.POST.get('gamemode')
	inputPassword: str = request.POST.get('lobbypassword')
	inputTimeamount: str = request.POST.get('timeamountfield')
	inputPlayeramount: str = request.POST.get('playeramountfield')
	inputQuestionamount: list = request.POST.get('questionamountfield')
	inputCategories = request.POST.getlist('categories')
	inputPending = request.POST.get("pending")
	# Check if user is logged in
	if not request.user.is_authenticated:
		args['errorMsg'] = 'User muss angemeldet sein um eine Lobby erstellen zu können'
		return createlobby_end(request, args)

	if is_lazy_user(request.user):
		args['errorMsg'] = 'Temporäre Benutzer können keine Lobbys erstellen.'
		return createlobby_end(request, args)

	# Check if POST request was initiated by form
	if not inputLobbycreate:
		args['errorMsg'] = 'Ein Fehler ist aufgetreten.'
		return createlobby_end(request, args)

	# Check number inputs
	if not inputTimeamount.isnumeric():
		args['errorMsg'] = 'Zeit muss eine Zahl sein.'
		return createlobby_end(request, args)
	time_amount = int(inputTimeamount)

	if not inputPlayeramount.isnumeric():
		args['errorMsg'] = 'Spieleranzahl muss eine Zahl sein.'
		return createlobby_end(request, args)
	player_amount = int(inputPlayeramount)

	if not inputQuestionamount.isnumeric():
		args['errorMsg'] = 'Fragenanzahl muss eine Zahl sein.'
		return createlobby_end(request, args)
	question_amount = int(inputQuestionamount)

	# Check other inputs
	if not inputGamemode or not inputLobbytype or not question_amount or not time_amount or not player_amount or not inputCategories:
		args['errorMsg'] = 'Eine der erforderlichen Felder wurde nicht ausgefüllt.'
		return createlobby_end(request, args)

	if len(inputCategories) < 1:
		args['errorMsg'] = 'Es muss mindestens eine Kategorie ausgewählt werden.'
		return createlobby_end(request, args)

	# Set default lobby name if nothing else was defined
	if not inputLobbyname:
		inputLobbyname = f"{request.user.username}'s Raum"
	else:
		if not check_valid_chars(inputLobbyname):
			args['errorMsg'] = 'Lobbyname enthält ungültige Zeichen.'
			createlobby_end(request, args)

	# Check bounds of number inputs
	if question_amount < 1 or question_amount > 64:
		args['errorMsg'] = 'Fragenanzahl außerhalb des erlaubten Bereichs.'
		return createlobby_end(request, args)

	if player_amount < 2 or player_amount > 16:
		args['errorMsg'] = 'Spieleranzahl außerhalb des erlaubten Bereichs.'
		return createlobby_end(request, args)
	if inputLobbytype.lower() == 'single':
		player_amount=1

	# Check if lobby type is valid
	if inputLobbytype.lower() in ['private', 'privat', 'single']:
		inputLobbytype = True
	else:
		inputLobbytype = False
	# Check if password is valid if password is defined
	if inputPassword is not None and inputPassword != '':
		password = b64encode(inputPassword)
	else:
		password = None

	gamemode_objset = LobbyType.objects.filter(LTname=inputGamemode)
	if len(gamemode_objset) < 1:
		args['errorMsg'] = 'ungültiger Spielemodus'
		return createlobby_end(request, args)

	# Create lobby auth token
	uuid_token = uuid.uuid4()
	unique = True
	lobby_key = ""
	counter = 0

	while unique:
		lobby_key = generate_lobby_key()
		if len(Lobby.objects.filter(Lkey=lobby_key)) == 0:
			unique = False
		else:
			counter += 1
			if counter >= 50:
				args[
					"errorMsg"] = 'Es ist ein Fehler bei der Lobbyerstellung aufgetreten. Bitte in wenigen Minuten erneut probieren.'
				return createlobby_end(request, args)

	usedquestions = []
	stateapproved = State.objects.filter(STid=1)
	statepending = State.objects.filter(~Q(STid=2))
	for cat in inputCategories:
		if inputPending:
			usedquestions.extend(Question.objects.filter(Q(Cid=cat) & Q(STid__in=statepending)).values_list('Qid', flat=True))
		else:
			usedquestions.extend(Question.objects.filter(Q(Cid=cat) & Q(STid__in=statepending)).filter().values_list('Qid', flat=True))
	questions_selected = choose_random(usedquestions, question_amount)

	if len(questions_selected ) < question_amount or len(questions_selected ) > question_amount:
		args["errorMsg"] = 'Es stehen nicht genug Fragen durch die ausgewählten Kategorien zur Verfügung.'
		return createlobby_end(request, args)

	# Create lobby
	lobby_obj = Lobby.objects.create(
		Uid=request.user, Lname=inputLobbyname, Ltype=gamemode_objset[0],
		Lplayerlimit=player_amount, Lpassword=password, Lauthtoken=uuid_token,
		Lkey=lobby_key, Lprivate=inputLobbytype, Lquestionamount=inputQuestionamount, Ltimeamount=inputTimeamount,
	)
	lobby_obj.save()
	for c in inputCategories:
		lc = LobbyCategory.objects.create(Lid=lobby_obj, Cid=Category.objects.get(Cid=c))
	for q in questions_selected:
		lq = LobbyQuestions.objects.create(Lid=lobby_obj, Qid=Question.objects.get(Qid=q))
		lq.save()

	return redirect(f'/lobby/{lobby_obj.Lkey}/{uuid_token}/')


def createlobby_end(request, args):
	if args is None or not args:
		args = {
			'errorMsg': '',
			'infoMsg': ''
		}
	return render(request, 'kwiss_it/createlobby.html', args)


def join_lobby(Lkey, user_obj: User, password=None, authtoken=None):
	# Get Lobby
	check_lazy_user(user_obj)
	lobby_objset = Lobby.objects.filter(Lkey=Lkey)
	if len(lobby_objset) < 1:
		return [False, 'Lobby konnte nicht gefunden werden.']

	# Get Lobbys of Player
	lobbyuser_objset = LobbyUser.objects.filter(Uid=user_obj)
	if len(lobbyuser_objset) > 0:
		return [False, 'Spieler ist bereits in einer Lobby.']

	lobby_obj = lobby_objset[0]
	test_valid = False
	if password:
		password=unquote(password)

		password=b64encode(password)
	if lobby_obj.is_full():
		return [False, 'Lobby ist bereits voll.']

	if lobby_obj.is_public_lobby():
		test_valid = True
	elif lobby_obj.is_private_lobby():
		test_valid = (lobby_obj.check_password(password) or lobby_obj.check_authtoken(authtoken))
	elif lobby_obj.is_solo_lobby():
		test_valid = lobby_obj.check_authtoken(authtoken)
	if test_valid:
		lobbyuser_obj = LobbyUser.objects.create(Lid=lobby_obj, Uid=user_obj)
		lobbyuser_obj.save()
		return [True, 'Lobby erfolgreich beigetreten.']
	else:
		return [False, 'Lobby konnte nicht beigetreten werden.']


@allow_lazy_user
def lobby_view(request, lobby_key, auth_token=None):
	check_old_heartbeat()
	#check_old_lobbys()
	args = {
		'errorMsg': '',
		'infoMsg': '',
	}
	passhash = request.GET.get('passhash')

	result = join_lobby(lobby_key, request.user, passhash, auth_token)

	if result[0]:
		args['auth_token'] = auth_token
		args['lobby_key'] = lobby_key
		lobby = Lobby.objects.get(Lkey=lobby_key)
		args['lobby_name'] = lobby.Lname
		args['userlimit'] = lobby.Lplayerlimit
		args['currentuser'] = len(LobbyUser.objects.filter(Lid=lobby))
		return render(request, 'kwiss_it/game.html', args)
	else:
		args['errorMsg'] = result[1]
		# TODO: Instead of redirecting. If player is already in lobby -> do rejoining?
		return render(request, 'kwiss_it/lobbylist.html', args)


@allow_lazy_user
def lobby_heartbeat_view(request, lobby_key):
	check_old_heartbeat()
	user = request.user

	lobbyuser_objset = LobbyUser.objects.filter(Lid__Lkey=lobby_key, Uid=user)
	if len(lobbyuser_objset) > 0:
		lobbyuser_obj = lobbyuser_objset[0]
		lobbyuser_obj.LPLastHeartbeat = datetime.now()
		lobbyuser_obj.save()
		name = user.username
		if user.first_name != '':
			name = user.first_name
		return JsonResponse({
			'status': 200,
			'name': name
		})

	return JsonResponse({
		'status': 403
	})

@allow_lazy_user
def lobby_ready_view(request, lobbykey, ready):
	check_old_heartbeat()
	user = request.user

	lobbyuser_objset = LobbyUser.objects.filter(Lid__Lkey=lobbykey, Uid=user)
	if len(lobbyuser_objset) > 0:
		lobbyuser_obj = lobbyuser_objset[0]
		lobbyuser_obj.LPLastHeartbeat = datetime.now()
		lobbyuser_obj.LPready = (ready == 'true')
		lobbyuser_obj.save()
		return JsonResponse({
			'status': 200
		})

	return JsonResponse({
		'status': 403
	})


def check_old_heartbeat():
	# Check if someone is still in Lobby but heartbeat missing for 15s
	# If thats the case remove user from lobby
	lobbyuser_objset = LobbyUser.objects.filter(LPLastHeartbeat__lt=(datetime.now() - timedelta(seconds=10)))
	lobbyuser_objset.delete()
	return


def check_old_lobbys():
	lobbyuser_objset = LobbyUser.objects.distinct()
	lobby_objset = Lobby.objects.filter(
		~Q(Lid__in=lobbyuser_objset) &
		Q(Lcreated__lte=(datetime.now() - timedelta(seconds=15)))
	)
	lobby_objset.delete()
	return



