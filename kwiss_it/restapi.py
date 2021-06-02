from django.db.models import Q
from .models import LobbyType, Lobby, LobbyPlayer, LobbyQuestions, Category, QuestionType, Question, Answer
from rest_framework import serializers, viewsets


# Lobby
class LobbySerializer(serializers.ModelSerializer):
	class Meta:
		model = Lobby
		fields = ['Lkey', 'Lname', 'Ltype', 'Lplayerlimit', 'Lprivate']


class LobbyView(viewsets.ReadOnlyModelViewSet):
	queryset = Lobby.objects.filter(Lstarted=False)
	serializer_class = LobbySerializer

	def get_queryset(self):
		queryset = Lobby.objects.filter(
			Q(Lstarted=False) &
			(
				Q(Lprivate=True) &
				Q(Lpassword__isnull=False) |
				Q(Lprivate=False)
			)
		)

		return queryset


class LobbyPlayerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Lobby
		fields = ['LPready']


class LobbyPlayerView(viewsets.ReadOnlyModelViewSet):
	queryset = LobbyPlayer.objects.all()
	serializer_class = LobbyPlayerSerializer

	def get_queryset(self):
		lobby_key = self.request.query_params.get('lkey')

		# Only allow if lobby_key is defined in api call
		if not lobby_key:
			return Lobby.objects.none()

		lobby_objset = Lobby.objects.filter(Lkey=lobby_key)

		if len(lobby_objset) < 1:
			# Lobby not found
			return Lobby.objects.none()

		queryset = LobbyPlayer.objects.filter(Lid=lobby_objset[0])
		return queryset


# Category
class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ['Cname', 'Cdescription', 'STid', 'Cupvotes', 'Cdownvotes']


class CategoryView(viewsets.ReadOnlyModelViewSet):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer

	def get_queryset(self):
		last_cname = self.request.query_params.get('lastcat')
		queryset = Category.objects.all().order_by('Cname')

		if last_cname:
			last_category = queryset.filter(Cname=last_cname)
			if len(last_category):
				queryset = queryset.filter(Cname__gt=last_cname)

		queryset = queryset[:15]
		return queryset


# Questions
class QuestionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Question
		fields = ['Qid', 'Qtext', 'QTid', 'Qplaycount', 'Qupvotes', 'Qdownvotes']


class QuestionView(viewsets.ReadOnlyModelViewSet):
	queryset = Question.objects.all()
	serializer_class = QuestionSerializer

	def get_queryset(self):
		question_id = self.request.query_params.get('qid')

		if question_id:
			# Return single question
			queryset = Question.objects.filter(Qid=question_id)
			if len(queryset) < 1:
				return Question.objects.none()
			return queryset[0]
		return Question.objects.none()


class QuestionTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = QuestionType
		fields = ['QTid', 'QTname', 'QTdescription']


class QuestionTypeView(viewsets.ReadOnlyModelViewSet):
	queryset = QuestionType.objects.all()
	serializer_class = QuestionTypeSerializer


# Answer
class AnswerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Answer
		fields = ['']

