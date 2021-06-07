from django.test import TestCase, Client
from django.urls import path
from . models import Lobby, User, Question, Answer, Category
from django.urls import reverse


class SeparateFileTest(TestCase):

	# Test that checks if the secret_key is in a separate file
	def test_is_secret_key_in_separate_file(self):
		filename = "kwiss/SECRET_KEY"
		message = "File not found"
		f = open(filename)
		self.assertTrue(f, message)

	# Test that checks if the database configuration is in a separate file
	def test_is_db_conf_in_separate_file(self):
		filename = "kwiss/my.cnf"
		message = "File not found"
		f = open(filename)
		self.assertTrue(f, message)

# Tests which verify that the pages can be loaded
class WebsiteLoadTest(TestCase):

	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(
			username='testi', password='Passwort123'
		)

	# Checks the home page
	def test_load_start_page(self):
		response = self.client.get(reverse('index'))
		self.assertEqual(200, response.status_code)

	# Checks the privacy page
	def test_load_datenschutz_page(self):
		response = self.client.get(reverse('datenschutz'))
		self.assertEqual(200, response.status_code)

	# Checks the imprint page
	def test_load_impressum_page(self):
		response = self.client.get(reverse('impressum'))
		self.assertEqual(200, response.status_code)

	# Checks the register page
	def test_load_register_page(self):
		response = self.client.get(reverse('register'))
		self.assertEqual(200, response.status_code)
		response = self.client.get('/register/checkusername', follow=True)
		self.assertEqual(200, response.status_code)
		response = self.client.get('/register/checkusername/test', follow=True)
		self.assertEqual(200, response.status_code)

	# Checks the login page
	def test_load_login_page(self):
		response = self.client.get(reverse('login'))
		self.assertEqual(200, response.status_code)

	# Checks the logout page
	def test_load_logout_page(self):
		response = self.client.get(reverse('logout'))
		self.assertEqual(200, response.status_code)

	# Checks the page where content can be added
	def test_load_addcontent_page(self):
		login = self.client.login(
			username='Testinger',
			password='Passwort123',
		)
		self.assertTrue(login)
		response = self.client.get(reverse('addcontent'))
		self.assertEqual(200, response.status_code)

	# Checks the page where the profile of the user "test" is displayed
	def test_load_test_user_page(self):
		response = self.client.get('/user/test')
		self.assertEqual(200, response.status_code)

	# Checks the page where a lobby can be created
	def test_load_createlobby_page(self):
		response = self.client.get('/createlobby')
		self.assertEqual(200, response.status_code)

	# Checks the page where existing lobbies can be displayed
	def test_load_lobbylist(self):
		response = self.client.get('/lobbylist')
		self.assertEqual(200, response.status_code)


class WebsiteTests(TestCase):

	# Instantiates an object of type Client in self.client and
	# creates a user "testi"
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(
			username='testi', password='Passwort123'
		)

	# Tests if the login via the login page works
	def test_login(self):
		response = self.client.get(reverse('login'), follow=True)
		self.assertEqual(response.status_code, 200)
		response = self.client.post(reverse('login'), {
			'inputUsername':	'testi',
			'inputPassword':	'Passwort123',
			'buttonLogin':		'buttonLogin'
		}, follow=True)
		self.assertContains(response, 'Login erfolgreich.')

	# Tests if the registration via the register page works.
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

	# Test to create a lobby
	def test_create_lobby(self):
		login = self.client.login(
			username='Testi',
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

	# Test to join a game
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
		self.assertContains(otherResponse, 'Lobbys')

	# Test that adds a new category to the database via the addcontent page
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

	# Test that adds a new question about the addcontent page,
	# where an exact number must be given.
	def test_insert_content_question_number_exact(self):
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
		self.assertNotContains(response, 'alert')
		questions = Question.objects.order_by('-Qid')
		self.assertNotIn(str(questions), 'Example Question')

	# Test that adds a new question with a correct answer via the addcontent page
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
			'questiontext1': 		'Example Question 2',
			'question1answertext0': 'Example Answer 2dot1',
			'question1answertext1': 'Example Answer 2dot2',
			'question1correct': 	'0',

			'buttoncreate': 'buttoncreate'
		})
		self.assertEqual(response.status_code, 200)
		self.assertNotContains(response, 'alert')
		questions = Question.objects.order_by('-Qid')
		self.assertNotIn(str(questions), 'Example Question 2')

	# Test that adds a new question with multiple correct answer via addcontent page
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
			'questiontext1': 		'Example Question 3',
			'question1answertext0': 'Example Answer 3dot1',
			'question1answertext1': 'Example Answer 3dot2',
			'question1correct0': 	'1',
			'question1correct1':	'1',

			'buttoncreate': 'buttoncreate'
		})
		self.assertEqual(response.status_code, 200)
		self.assertNotContains(response, 'alert')
		questions = Question.objects.order_by('-Qid')
		self.assertNotIn(str(questions), 'Example Question 3')
