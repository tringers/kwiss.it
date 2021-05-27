import string
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def index(request):
    return render(request, 'kwiss_it/index.html')


def datenschutz(request):
    return render(request, 'kwiss_it/datenschutz.html')


def impressum(request):
    return render(request, 'kwiss_it/impressum.html')


def lobby(request, lobby_id):
    return render(request, 'kwiss_it/lobby.html')


def settings(request):
    return render(request, 'kwiss_it/settings.html')


def register(request):
    args = {
        'errorMsg': '',
        'infoMsg': ''
    }

    if request.user.is_authenticated:
        args['errorMsg'] = 'Logged in'
        return register_end(request, args)

    if request.method == 'POST':
        buttonRegister = request.POST.get('buttonRegister')
        inputEmail = request.POST.get('inputEmail').lower()
        inputUsername = request.POST.get('inputUsername')
        inputPassword = request.POST.get('inputPassword')
        inputPassword2 = request.POST.get('inputPassword2')

        # Check if everything was entered
        if not buttonRegister or not inputEmail or not inputUsername or not inputPassword or not inputPassword2:
            args['errorMsg'] = 'One of the required values were not present'
            return register_end(request, args)

        # Check min max length of username, email address and password
        if len(inputEmail) < 6 or len(inputEmail) > 320:
            args['errorMsg'] = 'Length of email address out of defined min/max'
            return register_end(request, args)

        if len(inputUsername) < 4 or len(inputUsername) > 64:
            args['errorMsg'] = 'Length of username out of defined min/max'
            return register_end(request, args)

        if len(inputPassword) < 8 or len(inputPassword) > 64:
            args['errorMsg'] = 'Length of password out of defined min/max'
            return register_end(request, args)

        # Check if username or email address exists
        try:
            user_obj = User.objects.get(email=inputEmail)
            args['errorMsg'] = 'Email address already in use'
            return register_end(request, args)
        except User.DoesNotExist:
            pass

        try:
            user_obj = User.objects.get(username=inputUsername)
            args['errorMsg'] = 'Username already in use'
            return register_end(request, args)
        except User.DoesNotExist:
            pass

        # Check if password meets requirements
        if inputPassword != inputPassword2:
            args['errorMsg'] = 'Passwords are not identical'
            return register_end(request, args)

        strength = 0

        # Check for digit char
        if any(char.isdigit() for char in inputPassword):
            strength += 1

        # Check for lowercase char
        if any(char.islower() for char in inputPassword):
            strength += 1

        # Check for uppercase char
        if any(char.isupper() for char in inputPassword):
            strength += 1

        # Check for special char
        punctuation_set = set(string.punctuation)
        if set(inputPassword).intersection(punctuation_set):
            strength += 1

        if strength < 3:
            args['errorMsg'] = 'Password does not meet requirements'
            return register_end(request, args)

        # TODO: Register user
        user_obj = User.objects.create_user(inputUsername, inputEmail, inputPassword)
        user_obj.save()
        args['infoMsg'] = 'Registered successfully, please log in'
        return register_end(request, args)

    return register_end(request, args)


def register_end(request, args=None):
    if args is None or not args:
        args = {
            'errorMsg': '',
            'infoMsg': ''
        }

    return render(request, 'kwiss_it/register.html', args)


def user(request):
    return render(request, 'kwiss_it/user.html')


def login(request, args=None):
    if args is None or not args:
        args = {
            'errorMsg': '',
            'infoMsg': ''
        }

    if request.method == 'POST':
        buttonLogin = request.POST.get('buttonLogin')
        inputUsername = request.POST.get('inputUsername')
        inputPassword = request.POST.get('inputPassword')
        user_obj = authenticate(request, username=inputUsername, password=inputPassword)

        if user_obj is not None:
            # Redirect to a success page.
            login(request, user_obj)
            args['infoMsg'] = 'Login Erfolgreich'
            pass
        else:
            # Return an 'invalid login' error message.
            args['errorMsg'] = 'Login Fehlgeschlagen'
            pass

    return render(request, 'kwiss_it/login.html', args)


def review(request):
    return render(request, 'kwiss_it/review.html')
