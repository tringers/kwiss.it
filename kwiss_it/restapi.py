from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

from .models import LobbyType, Lobby, LobbyPlayer, LobbyQuestions, Category, QuestionType, Question, Answer
from rest_framework import serializers, viewsets, mixins, generics


# Lobby
class LobbySerializer(serializers.ModelSerializer):
	class Meta:
		model = Lobby
		fields = ['Lkey', 'Lname', 'Ltype', 'Lplayerlimit', 'Lprivate']


class LobbyView(viewsets.ReadOnlyModelViewSet):
	queryset = Lobby.objects.filter(Lstarted=False)
	serializer_class = LobbySerializer

	def get_queryset(self):
		lobby_key = self.request.query_params.get('lkey')

		if not lobby_key:
			queryset = Lobby.objects.filter(
				Q(Lstarted=False) &
				(
						Q(Lprivate=True) &
						Q(Lpassword__isnull=False) |
						Q(Lprivate=False)
				)
			)
		else:
			queryset = Lobby.objects.filter(Lkey=lobby_key)

		return queryset


class LobbyPlayerSerializer(serializers.ModelSerializer):
	first_name = serializers.StringRelatedField(source='Uid', read_only=True)

	class Meta:
		model = LobbyPlayer
		fields = ['first_name', 'LPready']


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


class LobbyTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = LobbyType
		fields = ['LTid', 'LTdescription']


class LobbyTypeView(viewsets.ReadOnlyModelViewSet):
	queryset = LobbyType.objects.all()
	serializer_class = LobbyTypeSerializer


# Category
class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ['Cname', 'Cdescription', 'STid', 'Cupvotes', 'Cdownvotes', 'Cid']


class CategoryView(mixins.ListModelMixin, viewsets.GenericViewSet):
	queryset = Category.objects.all().order_by('Cname')
	serializer_class = CategorySerializer
	pagination_class = PageNumberPagination


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
