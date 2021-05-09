from django.test import TestCase, Client
from django.urls import path


class SecretKeyTest(TestCase):

	def test_is_secret_key_in_seprate_file(self):
		filename = "kwiss/SECRET_KEY"
		message = "File not found"
		f = open(filename)
		self.assertTrue(f, message)



class WebsiteTest(TestCase):

	def test_load_start_page(self):
		client = Client()
		response = client.get('/')
		self.assertEqual(200, response.status_code)

	def test_load_hello_leduc(self):
		client = Client()
		response = client.get('/Le Duc/')
		self.assertIn(b"Hello Le Duc!", response.content)

	def test_load_hello_sascha(self):
		client = Client()
		response = client.get('/Sascha/')
		self.assertIn(b"Hello Sascha!", response.content)

	def test_load_hello_timo(self):
		client = Client()
		response = client.get('/Timo/')
		self.assertIn(b"Hello Timo!", response.content)
