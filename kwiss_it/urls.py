from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('datenschutz', views.datenschutz, name='datenschutz'),
    path('impressum', views.impressum, name='impressum'),
    re_path(r'(?P<lobby_id>[0-9A-F]{6})/$', views.lobby, name='lobby'),

    path('settings', views.settings, name='settings'),
    path('review', views.review, name='review'),

    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('password-reset', views.login, name='vergessen'),
    path('user', views.user, name='user'),
]
