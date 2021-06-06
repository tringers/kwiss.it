from django.test import TestCase, Client
from django.urls import path
from . models import Lobby
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

	def test_load_password_reset_page(self):
		client = Client()
		response = client.get('/password-reset')
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

	def test_login(self):
		client = Client()
		response = client.post(reverse('login'), {
			'inputUsername':	'test',
			'inputPassword':	'Test123'
		})
		self.assertContains(response, b'Login fehlgeschlagen.')

	def test_register(self):
		client = Client()
		response = client.post(reverse('register'),{
			'inputEmail':		'example@example.com',
			'inputUsername': 	'Testinger',
			'inputName': 		'Tester',
			'inputPassword':	'Passwort123',
			'inputPassword2':	'Passwort123'
		})
		self.assertEqual(200, response.status_code)
		client.login(username='Testinger', password='Passwort123')
		client.get(reverse('index'))
		self.assertContains(client, b'Spiel erstellen')

class DatabaseTest(TestCase):

	def test_default_lobby_is_private(self):
		lobby = Lobby()
		self.assertIs(lobby.is_private_lobby(), False)

	def test_lobby_is_public(self):
		lobby = Lobby(Lprivate=True)
		self.assertIs(lobby.is_private_lobby(), True)