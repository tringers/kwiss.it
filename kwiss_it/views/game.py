from .helper import *

# TODO: Helper functions and checks
# 		Run these before processing anything else
# TODO: Use Lobby.Uid for Solo Lobby!

def setCurrentQuestion():
	# Check here, if lobby's currentQuestion is up-to-date
	return

def heartbeatCheck():
	# Check users last_heartbeat and kick him if necessary
	return


def game_update(request, lobbykey):
	if request.method == 'POST':
		return answerSubmit(request, lobbykey)
	else:
		return getScores(request, lobbykey)


def answerSubmit(request, lobby_key):
	data = {
		'status': 200,
		'message': '',
		'lastSubmissionCorrect': False,
		'deviation': 0,
		'checkLater': False,
		'addition': 0,
		'streak': 0,
		'score': 0,
	}

	answer = json.loads(request.body)
	user = request.user
	a_authkey = answer['lobbyAuth']
	a_name = answer['name']
	a_question = answer['qno']
	a_answer = answer['answer']

	# Securitycheck
	lobby_objset = Lobby.objects.filter(Lkey=lobby_key, Lauthtoken=a_authkey)

	if user.first_name != a_name:
		data['status'] = 400
		data['message'] = 'Exception: CHECK_first_name'

	if len(lobby_objset) < 1:
		data['status'] = 400
		data['message'] = 'Exception: CHECK_find_lobby'

	if data['status'] != 400:
		lobby_obj = lobby_objset[0]
		lq_objset = LobbyQuestions.objects.filter(Lid=lobby_obj)

		if not lq_objset[a_question - 1]:
			data['status'] = 400
			data['message'] = 'Exception: CHECK_find_question'
		else:
			lq_obj = lq_objset[a_question - 1]
			q_obj = lq_obj.Qid
			a_objset = Answer.objects.filter(Qid=q_obj, Acorrect=True)

			if q_obj.QTid == 1:
				# Number correct
				if int(a_objset[0].Atext) == int(a_answer[0]):
					data['lastSubmissionCorrect'] = True
			elif q_obj.QTid == 2:
				# Single correct
				if int(a_objset[0].Anum) == int(a_answer[0]):
					data['lastSubmissionCorrect'] = True
			elif q_obj.QTid == 3:
				# Multiple correct
				correct = True
				if len(a_objset) != len(a_answer):
					correct = False

				if correct:
					for i in range(len(a_answer)):
						userAnswer = a_answer[i]
						found = False

						for j in range(len(a_objset)):
							answer = a_objset[j]
							if int(userAnswer) == int(answer.Anum):
								found = True
								break

						if not found:
							correct = False
							break

				data['lastSubmissionCorrect'] = correct
			elif q_obj.QTid == 4:
				# Deviation
				data['lastSubmissionCorrect'] = True
				if a_answer[0] == -1:
					data['deviation'] = -1
				else:
					data['deviation'] = abs(int(a_objset[0].Atext) - int(a_answer[0]))

	if data['status'] != 400:
		lq_obj = lq_objset[a_question - 1]
		q_obj = Question.objects.get(Qid=lq_obj.Qid)
		lu_objset = LobbyUser.objects.filter(Lid=lobby_obj, Uid=user)

		if len(lu_objset) < 1:
			data['status'] = 400
			data['message'] = 'Exception: CHECK_find_lobbyuser'
		else:
			lu_obj = lu_objset[0]
			lu_obj.LPdeviation = data['deviation'] | 0
			lu_obj.LPquestionanswered = q_obj
			lu_obj.LPwasdeviation = False
			lu_obj.save()
			data['checkLater'] = True

			if q_obj.QTid == 4:
				lu_obj.LPwasdeviation = True
				lu_obj.save()

				# Check if everybody has submitted
				lu_objset_all = LobbyUser.objects.filter(Lid=lobby_obj)
				allAnswered = True
				for lu_obj_all in lu_objset_all:
					if lu_obj_all.LPquestionanswered != q_obj:
						allAnswered = False

				if allAnswered:
					lu_objset_all = LobbyUser.objects.filter(Lid=lobby_obj, LPdeviation__gte=0).order_by('LPdeviation')
					lu_objset_all = lu_objset_all | LobbyUser.objects.filter(Lid=lobby_obj, LPdeviation=-1)
					# Calculate points
					first = True
					points = lu_objset_all + 1

					for lu_obj_all in lu_objset_all:
						if lu_obj_all.LPdeviation == -1:
							# Oof, player's wrong
							lu_obj_all.LPStreak = 0
							lu_obj_all.LPScore += 0
							lu_obj_all.LPlastaddition = 0
							pass
						else:
							if first:
								# Increase Streak for first correct
								lu_obj_all.LPStreak += 1
								lu_obj_all.LPScore += points
								lu_obj_all.LPlastaddition = points
								points -= 1
							else:
								# Add points for every other but no streak increase
								lu_obj_all.LPStreak += 0
								lu_obj_all.LPScore += points
								lu_obj_all.LPlastaddition = points

							points -= 1
							lu_obj_all.save()
			else:
				if data['lastSubmissionCorrect']:
					lu_obj.Streak += 1
				else:
					lu_obj.Streak = 0
				lu_obj.LPlastaddition = lu_obj.Streak
				lu_obj.LPscore += lu_obj.Streak
				lu_obj.save()
				data['addition'] = lu_obj.Streak
				data['streak'] = lu_obj.Streak
				data['score'] = lu_obj.LPscore

	return JsonResponse(data)


def getScores(request, lobby_key):
	# TODO: Spieler statt hiermit in einer späteren Version von der API abfragen lassen
	# Dafür muss LobbyUser die aktuelle Frage des Spielers kennen
	data = {
		'status': 200,
		'message': '',
		'deviation': False,
		'results': [],
	}
	template = {
		'name': '',
		'addition': 0,
		'streak': 0,
		'score': 0,
	}

	user = request.user

	# Check for "lu_obj.LPwasdeviation" => All data
	# "!lu_obj.LPwasdeviation" => Others data

	data['results'].append(template.copy())

	return JsonResponse(data)


