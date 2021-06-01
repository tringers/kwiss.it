from django.test import TestCase, Client
from django.urls import path


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
		response = client.get('/')
		self.assertEqual(200, response.status_code)

	def test_load_datenschutz_page(self):
		client = Client()
		response = client.get('/datenschutz')
		self.assertEqual(200, response.status_code)

	def test_load_impressum_page(self):
		client = Client()
		response = client.get('/impressum')
		self.assertEqual(200, response.status_code)

	def test_load_login_page(self):
		client = Client()
		response = client.get('/login')
		self.assertEqual(200, response.status_code)

	def test_load_logout_page(self):
		client = Client()
		response = client.get('/logout')
		self.assertEqual(200, response.status_code)

	def test_load_register_page(self):
		client = Client()
		response = client.get('/register')
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