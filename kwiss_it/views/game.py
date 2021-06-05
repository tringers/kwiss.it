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


def game_update(request, lobby_key):
	if request.method == 'POST':
		return answerSubmit(request, lobby_key)
	else:
		return getScores(request, lobby_key)


def answerSubmit(request, lobby_key):
	data = {
		'lastSubmissionCorrect': False,
		'addition': 0,
		'streak': 0,
		'score': 0,
	}

	answer = request.body

	return JsonResponse(data)


def getScores(request, lobby_key):
	# TODO: Spieler statt hiervon in einer späteren Version von der API abfragen lassen
	# Dafür muss LobbyUser die aktuelle Frage des Spielers kennen

	data = []
	template = {
		'name': '',
		'addition': 0,
		'streak': 0,
		'score': 0,
	}

	data.append(template.copy())

	return JsonResponse(data)


