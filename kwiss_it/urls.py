from django.urls import path, re_path, include
from rest_framework import routers
from . import views
from . import restapi


router = routers.DefaultRouter()
router.register(r'lobby', restapi.LobbyView)
router.register(r'lobbyplayer', restapi.LobbyPlayerView)
router.register(r'category', restapi.CategoryView)
router.register(r'question', restapi.QuestionView)
router.register(r'questiontype', restapi.QuestionTypeView)


urlpatterns = [
	path('', views.index, name='index'),
	path('datenschutz', views.datenschutz, name='datenschutz'),
	path('impressum', views.impressum, name='impressum'),
	re_path(r'(?P<lobby_id>[0-9A-F]{6})/$', views.lobby, name='lobby'),

	path('settings', views.settings, name='settings'),
	path('review', views.review, name='review'),

	path('login', views.login_view, name='login'),
	path('logout', views.logout_view, name='logout'),
	path('register', views.register, name='register'),
	path('register/checkusername/', views.register_checkusername_short, name='register_checkusername_short'),
	path('register/checkusername/<str:username>', views.register_checkusername, name='register_checkusername'),
	path('password-reset', views.login, name='vergessen'),
	path('u', views.user, name='userShort'),
	path('u/', views.user, name='userShort'),
	path('u/<str:username>', views.user_short, name='userShort'),
	path('user', views.user, name='user'),
	path('user/', views.user, name='user'),
	path('user/<str:username>', views.user_profile, name='userProfile'),
	path('createlobby', views.createlobby_view, name='createlobby'),
	path('api/', include(router.urls)),
]
