from django.test import TestCase, Client
from django.urls import path
from . models import Lobby, User
from django.urls import reverse


class SeparateFileTest(TestCase):

	def test_is_secret_key_in_separate_file(self):
		filename = "kwiss/SECRET_KEY"
		message = "File not found"
		f = open(filename)
		self.assertTrue(f, message)

	def test_is_db_conf_in_separate_file(self):
		filename = "kwiss/my.cnf"
		message = "File not found"
		f = open(filename)
		self.assertTrue(f, message)


class WebsiteLoadTest(TestCase):

	def test_load_start_page(self):
		client = Client()
		response = client.get(reverse('index'))
		self.assertEqual(200, response.status_code)

	def test_load_datenschutz_page(self):
		client = Client()
		response = client.get(reverse('datenschutz'))
		self.assertEqual(200, response.status_code)

	def test_load_impressum_page(self):
		client = Client()
		response = client.get(reverse('impressum'))
		self.assertEqual(200, response.status_code)

	def test_load_login_page(self):
		client = Client()
		response = client.get(reverse('login'))
		self.assertEqual(200, response.status_code)

	def test_load_logout_page(self):
		client = Client()
		response = client.get(reverse('logout'))
		self.assertEqual(200, response.status_code)

	def test_load_register_page(self):
		client = Client()
		response = client.get(reverse('register'))
		self.assertEqual(200, response.status_code)

	def test_load_user_page(self):
		client = Client()
		response = client.get('/user/test')
		self.assertEqual(200, response.status_code)

	def test_load_createlobby_page(self):
		client = Client()
		response = client.get('/createlobby')
		self.assertEqual(200, response.status_code)

	def test_load_lobbylist(self):
		client = Client()
		response = client.get('/lobbylist')
		self.assertEqual(200, response.status_code)


class WebsiteTests(TestCase):

	# def setUp(self):
	# 	self.client = Client()
	# 	self.user = User.objects.create_user(
	# 		username='testinger', password='Passwort123'
	# 	)

	def test_login(self):
		response = self.client.get(reverse('login'), follow=True)
		self.assertEqual(response.status_code, 200)
		response = self.client.post(reverse('login'), {
			'inputUsername':	'testinger',
			'inputPassword':	'Passwort123',
			'buttonLogin':		'buttonLogin'
		}, follow=True)
		self.assertContains(response, 'Login erfolgreich.')

	# def test_register(self):
	# 	response = self.client.post(reverse('register'),{
	# 		'inputEmail':		'example@example.com',
	# 		'inputUsername': 	'Testinger',
	# 		'inputName': 		'Tester',
	# 		'inputPassword':	'Passwort123',
	# 		'inputPassword2':	'Passwort123',
	# 		'buttonRegister':	'buttonRegister'
	# 	})
	# 	self.assertEqual(response.status_code, 200)
	# 	# self.assertContains(response, '')
	# 	login = self.client.login(
	# 		username='Testinger',
	# 		password='Passwort123')
	# 	self.assertTrue(login)
	# 	response = self.client.get(reverse('index'))
	# 	self.assertEqual(response.status_code, 200)
	# 	self.assertContains(response, 'Spiel erstellen')

	def test_create_lobby(self):
		login = self.client.login(
			username='Testinger',
			password='Passwort123',
		)
		self.assertTrue(login)
		response = self.client.post(reverse('createlobby'), {
			'createlobbyname':		'testname',
			'lobbytype':			'public',
			'gamemode':				'basic',
			'pending':				'True',
			'playeramountfield':	'4',
			'questionamountfield':	'5',
			'timeamountfield':		'10',
			'categories':			'1',
			'buttoncreate':			'buttoncreate'
		}, follow=True)
		print("Response: {}".format(response.content))
		self.assertContains(response, 'Lobby:')

	def test_join_game(self):
		pass


# class DatabaseTest(TestCase):
#
# 	def test_default_lobby_is_private(self):
# 		lobby = Lobby()
# 		self.assertIs(lobby.is_private_lobby(), False)
#
# 	def test_lobby_is_public(self):
# 		lobby = Lobby(Lprivate=True)
# 		self.assertIs(lobby.is_private_lobby(), True)