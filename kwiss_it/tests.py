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

	def test_load_base_template(self):
		client = Client()
		response = client.get('/temp')
		self.assertEqual(301, response.status_code)
