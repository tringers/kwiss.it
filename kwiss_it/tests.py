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


class WebsiteTest(TestCase):

	def test_load_start_page(self):
		client = Client()
		response = client.get('/')
		self.assertEqual(200, response.status_code)

