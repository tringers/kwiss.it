from django.test import TestCase
from django.urls import path
from django.utils import timezone
import os.path

class SecretKeyTest(TestCase):

	def test_is_secret_key_in_seprate_file(self):
		filename = "kwiss/SECRET_KEY"
		message = "File not found"
		f = open(filename)
		self.assertTrue(f, message)



