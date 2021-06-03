from django.contrib.auth.forms import UserCreationForm as UserCreationFormBase
from django import forms

from .helper import *


class UserCreationForm(UserCreationFormBase):
	email = forms.EmailField(label="Email Adresse")
	first_name = forms.CharField(label="Anzeigename")

	class Meta:
		model = User
		fields = ("username", "first_name", "email")

	def get_credentials(self):
		return {
			'username': self.cleaned_data['username'],
			'email': self.cleaned_data['email'],
			'first_name': self.cleaned_data['first_name'],
			'password': self.cleaned_data['password1']
		}
