from django.test import TestCase, Client
from django.urls import path
from . models import Lobby, User, Question, Answer, Category
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


# TODO Durchscha ob es noch Seiten zu prüfen gibt
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

	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(
			username='testi', password='Passwort123'
		)

	def test_login(self):
		response = self.client.get(reverse('login'), follow=True)
		self.assertEqual(response.status_code, 200)
		response = self.client.post(reverse('login'), {
			'inputUsername':	'testi',
			'inputPassword':	'Passwort123',
			'buttonLogin':		'buttonLogin'
		}, follow=True)
		self.assertContains(response, 'Login erfolgreich.')


	def test_register(self):
		response = self.client.post(reverse('register'), {
			'inputEmail':		'example@example.com',
			'inputUsername': 	'Testi',
			'inputName': 		'Tester',
			'inputPassword':	'Passwort123',
			'inputPassword2':	'Passwort123',
			'buttonRegister':	'Registrieren'
		}, follow=True)
		self.assertEqual(response.status_code, 200)
		login = self.client.login(
			username='Testi',
			password='Passwort123')
		self.assertTrue(login)


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
		self.assertContains(response, 'Lobby:')

	# TODO Weis nicht genau, wie man den Lobbycode auslesen kann...
	def test_join_game(self):
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
		self.assertContains(response, 'Lobby:')

		otherClient = Client()
		otherResponse = otherClient.get(reverse('lobbylist'))
		text = str(otherResponse.content)
		num = text.find("/lobby/")
		# self.assertEqual(100, num)

	def test_insert_content_category(self):
		login = self.client.login(
			username='Testinger',
			password='Passwort123',
		)
		self.assertTrue(login)
		response = self.client.post(reverse('addcontent'), {
			'category':		'new',
			'catname':		'Test Name',
			'catdesc':		'Test Description',
			'buttoncreate':	'Erstellen'
		})
		self.assertEqual(response.status_code, 200)

		category = Category.objects.order_by('-Cid')[:1]
		self.assertIn(str(category[0]), 'Test Name')


	def test_insert_content_question_number_excat(self):
		login = self.client.login(
			username='Testinger',
			password='Passwort123',
		)
		self.assertTrue(login)
		response = self.client.post(reverse('addcontent'), {
			'category':				'1',
			'catname':				'',
			'catdesc':				'',

			'qtype1':				'number_exact',
			'questiontext1':		'Example Question',
			'question1answertext0':	'1234',

			'buttoncreate':			'buttoncreate'
		})
		self.assertEqual(response.status_code, 200)
		print("Response: {}".format(response.content))
		# TODO Funktioniert theoretisch.
		#  Nur Praktisch tauchen die Einträge nicht in der DB auf
		questions = Question.objects.order_by('-Qid')
		for question in questions:
			print("Question1: {}".format(question))

	def test_insert_content_question_single(self):
		login = self.client.login(
			username='Testinger',
			password='Passwort123',
		)
		self.assertTrue(login)
		response = self.client.post(reverse('addcontent'), {
			'category': 			'1',
			'catname': 				'',
			'catdesc': 				'',

			'qtype1': 				'single',
			'answeramount1': 		'2',
			'questiontext1': 		'Example Question2',
			'question1answertext0': 'Example Answer 2dot1',
			'question1answertext1': 'Example Answer 2dot2',
			'question1correct': 	'0',

			'buttoncreate': 'buttoncreate'
		})
		self.assertEqual(response.status_code, 200)
		print("Response: {}".format(response.content))
		# TODO Funktioniert theoretisch.
		#  Nur Praktisch tauchen die Einträge nicht in der DB auf
		questions = Question.objects.order_by('-Qid')
		for question in questions:
			print("Question2: {}".format(question))

	def test_insert_content_question_multiple(self):
		login = self.client.login(
			username='Testinger',
			password='Passwort123',
		)
		self.assertTrue(login)
		response = self.client.post(reverse('addcontent'), {
			'category': 			'1',
			'catname': 				'',
			'catdesc': 				'',

			'qtype1': 				'multiple',
			'answeramount1': 		'2',
			'questiontext1': 		'Example Question3',
			'question1answertext0': 'Example Answer 3dot1',
			'question1answertext1': 'Example Answer 3dot2',
			'question1correct0': 	'1',
			'question1correct1':	'1',

			'buttoncreate': 'buttoncreate'
		})
		self.assertEqual(response.status_code, 200)
		print("Response: {}".format(response.content))
		# TODO Funktioniert theoretisch.
		#  Nur Praktisch tauchen die Einträge nicht in der DB auf
		questions = Question.objects.order_by('-Qid')
		for question in questions:
			print("Question3: {}".format(question))

	def test_insert_content_question_number_deviation(self):
		login = self.client.login(
			username='Testinger',
			password='Passwort123',
		)
		self.assertTrue(login)
		response = self.client.post(reverse('addcontent'), {
			'category': 			'1',
			'catname': 				'',
			'catdesc': 				'',

			'qtype1': 				'number_deviation',
			'questiontext1': 		'Example Question4',
			'question1answertext0': '4321',

			'buttoncreate': 'buttoncreate'
		})
		self.assertEqual(response.status_code, 200)
		print("Response: {}".format(response.content))
		# TODO Funktioniert theoretisch.
		#  Nur Praktisch tauchen die Einträge nicht in der DB auf
		questions = Question.objects.order_by('-Qid')
		for question in questions:
			print("Question4: {}".format(question))

# TODO Weis nicht, ob es sinnvoll ist die auszubauen.
# class DatabaseTest(TestCase):
#
# 	def test_default_lobby_is_private(self):
# 		lobby = Lobby()
# 		self.assertIs(lobby.is_private_lobby(), False)
#
# 	def test_lobby_is_public(self):
# 		lobby = Lobby(Lprivate=True)
# 		self.assertIs(lobby.is_private_lobby(), True)