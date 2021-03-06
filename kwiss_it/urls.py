from django.urls import path, re_path, include
from rest_framework import routers
from django.views.generic import TemplateView
from .views import static, register, login, user, lobby, content, game,vote, moderator
from . import restapi

router = routers.DefaultRouter()
router.register(r'lobby', restapi.LobbyView)
router.register(r'lobbydata', restapi.LobbyDataView)
router.register(r'lobbyuser', restapi.LobbyUserView)
router.register(r'lobbytype', restapi.LobbyTypeView)
router.register(r'lobbyquestions', restapi.LobbyQuestionsView)
router.register(r'category', restapi.CategoryView)
router.register(r'question', restapi.QuestionView)
router.register(r'questiontype', restapi.QuestionTypeView)
router.register(r'answer', restapi.AnswerView)

urlpatterns = [
	# Static pages
	path('', static.index, name='index'),
	path('datenschutz', static.datenschutz, name='datenschutz'),
	path('impressum', static.impressum, name='impressum'),

	# Without any usage atm
	path('settings', static.settings, name='settings'),
	path('review', static.review, name='review'),

	# For new users
	path('register', register.register, name='register'),
	path('register/checkusername/', register.register_checkusername_short, name='register_checkusername_short'),
	path('register/checkusername/<str:username>', register.register_checkusername, name='register_checkusername'),

	# For registered users
	path('login', login.login_view, name='login'),
	path('logout', login.logout_view, name='logout'),
	# TODO: Create forgot-password page (create model for confirmation links in mail)
	path('addcontent', content.add_content, name='addcontent'),
	# path('password-reset', login.login, name='vergessen'),

	# For authenticated users
	path('u', user.user_view, name='userShort'),
	path('u/', user.user_view, name='userShort'),
	path('u/<str:username>', user.user_short_view, name='userShort'),
	path('user', user.user_view, name='user'),
	path('user/', user.user_view, name='user'),
	path('user/<str:username>', user.user_profile_view, name='userProfile'),

	# Gameplay
	path('createlobby', lobby.createlobby_view, name='createlobby'),
	path('lobbylist', lobby.lobbylist_view, name='lobbylist'),
	re_path(r'lobby/(?P<lobby_key>[0-9A-F]{6})/$', lobby.lobby_view, name='lobby'),
	re_path(r'lobby/(?P<lobby_key>[0-9A-F]{6})/(?P<auth_token>[0-9a-f\-]{0,36})/$', lobby.lobby_view, name='lobby'),
	re_path(r'lobby/heartbeat/(?P<lobby_key>[0-9A-F]{6})/$', lobby.lobby_heartbeat_view, name='lobby_heartbeat'),
	path('lobby/ready/<str:lobbykey>/<str:ready>', lobby.lobby_ready_view, name='lobby_ready'),

	path('game/<str:lobbykey>', game.game_update, name='game_update'),

	# API access
	path('api/', include(router.urls)),

	#voting
	path('vote/category/<int:cat_id>/<int:vote>', vote.voteCat,name='vote'),
	path('vote/question/<int:q_id>/<int:vote>', vote.voteQuestion,name='vote'),
	path(r'state/category/<int:c_id>/<str:state>',vote.stateCategory),
	path(r'state/question/<int:q_id>/<str:state>',vote.stateQuestion),


	#moderator
	path('moderator',moderator.moderator_view,name='moderator')

]
