from django.urls import path, re_path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('datenschutz', views.datenschutz, name='datenschutz'),
	path('impressum', views.impressum, name='impressum'),
	re_path(r'lobby/(?P<lobby_key>[0-9A-F]{6})/$', views.lobby_view, name='lobby'),
	re_path(r'lobby/(?P<lobby_key>[0-9A-F]{6})/(?P<auth_token>[0-9a-f\-]{0,36})/$', views.lobby_view, name='lobby'),

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
	path('lobbylist',views.lobbylist_view,name='lobbylist'),
]
