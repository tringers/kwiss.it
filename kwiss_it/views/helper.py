import random
import base64
import re
import string
import uuid
from datetime import datetime
from urllib.parse import unquote

from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from ratelimit.decorators import ratelimit
from lazysignup.decorators import allow_lazy_user, require_lazy_user, require_nonlazy_user
from lazysignup.utils import is_lazy_user

from ..models import UserLastSeen, UserPrivate, UserPicture, UserDescription, Picture, Lobby, LobbyPlayer, LobbyType


forbidden_usernames = [
	'user',
	'username',
	'admin',
	'administrator',
	'mod',
	'moderator',
	'test',
]

allow_chars_for_email = r'^[a-z0-9.!#$%&\'*+-/=?^_`{|}~@]+$'


def check_valid_chars(inputStr: str) -> bool:
	if not re.match("^[A-Za-z0-9 _!§$%&/()=?+#*'~,.;:-]*$", inputStr):
		return False
	return True


def generate_lobby_key():
	key_int = random.randint(pow(16, 5), pow(16, 6) - 1)
	key = '{0:06x}'.format(key_int).upper()
	return key


def check_user_last_seen(request):
	if not request.user.is_authenticated or is_lazy_user(request.user):
		return

	username = request.user.username
	user_objset = User.objects.filter(username=username)

	if len(user_objset) < 1:
		return

	user_obj = user_objset[0]

	uls_objset = UserLastSeen.objects.filter(Uid=user_obj)

	if len(uls_objset) < 1:
		uls_obj = UserLastSeen.objects.create(Uid=user_obj)
		uls_obj.save()
		pass
	else:
		uls_obj = uls_objset[0]
		uls_obj.LastSeen = datetime.now()

	return


def b64encode(text):
	return base64.b64encode(text.encode(encoding='utf-8')).decode(encoding='utf-8')


def b64decode(text):
	return base64.b64decode(text.encode(encoding='utf-8')).decode(encoding='utf-8')
