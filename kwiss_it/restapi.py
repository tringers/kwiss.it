from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import LobbyType, Lobby, LobbyUser, LobbyQuestions, Category, QuestionType, Question, Answer
from rest_framework import serializers, viewsets, mixins, generics, pagination


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


class LobbyDataSerializer(serializers.ModelSerializer):
	class Meta:
		model = Lobby
		fields = ['Lkey', 'Lname', 'Ltype', 'Lplayerlimit', 'Lquestionamount', 'Ltimeamount', 'LcurrentQuestion', 'LcurrentCorrect']


class LobbyDataView(viewsets.ReadOnlyModelViewSet):
	queryset = Lobby.objects.filter(Lstarted=False)
	serializer_class = LobbyDataSerializer

	def get_queryset(self):
		lobby_key = self.request.query_params.get('lkey')

		if not lobby_key:
			return Lobby.objects.none()
		else:
			return Lobby.objects.filter(Lkey=lobby_key)


class LobbyUserSerializer(serializers.ModelSerializer):
	first_name = serializers.SlugRelatedField(source='Uid', read_only=True, slug_field='first_name')

	class Meta:
		model = LobbyUser
		fields = ['first_name', 'LPready', 'LPScore', 'LPStreak']


class LobbyUserView(viewsets.ReadOnlyModelViewSet):
	queryset = LobbyUser.objects.all()
	serializer_class = LobbyUserSerializer

	def get_queryset(self):
		lobby_key = self.request.query_params.get('lkey')

		# Only allow if lobby_key is defined in api call
		if not lobby_key:
			return Lobby.objects.none()

		lobby_objset = Lobby.objects.filter(Lkey=lobby_key)

		if len(lobby_objset) < 1:
			# Lobby not found
			return Lobby.objects.none()

		queryset = LobbyUser.objects.filter(Lid=lobby_objset[0])
		return queryset


class LobbyTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = LobbyType
		fields = ['LTid', 'LTdescription']


class LobbyTypeView(viewsets.ReadOnlyModelViewSet):
	queryset = LobbyType.objects.all()
	serializer_class = LobbyTypeSerializer


class LobbyQuestionsSerializer(serializers.ModelSerializer):
	class Meta:
		model = LobbyQuestions
		fields = ['Qid']


class LobbyQuestionsView(viewsets.ReadOnlyModelViewSet):
	queryset = LobbyQuestions.objects.all()
	serializer_class = LobbyQuestionsSerializer

	def get_queryset(self):
		lobby_key = self.request.query_params.get('lkey')
		lobby_objset = Lobby.objects.filter(Lkey=lobby_key)

		if len(lobby_objset) > 0:
			queryset = LobbyQuestions.objects.filter(Lid=lobby_objset[0])
			return queryset

		return LobbyQuestions.objects.none()


# Category
class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ['Cname', 'Cdescription', 'STid', 'Cid']


class CustomPagination(pagination.PageNumberPagination):
	def get_paginated_response(self, data):
		return Response({
			'count': self.page.paginator.count,
			'next': self.get_next_link(),
			'previous': self.get_previous_link(),
			'results': data
		})


class CategoryView(mixins.ListModelMixin, viewsets.GenericViewSet):
	queryset = Category.objects.all().order_by('STid').order_by('Cname')
	serializer_class = CategorySerializer
	pagination_class = CustomPagination

	def get_queryset(self):
		state_id = self.request.query_params.get('stid')
		approved = self.request.query_params.get('approved')
		denied = self.request.query_params.get('denied')
		pending = self.request.query_params.get('pending')

		in_filter = []

		queryset = Category.objects.all().order_by('STid').order_by('Cname')

		if approved is None:
			approved = 'true'

		if denied is None:
			denied = 'false'

		if pending is None:
			pending = 'false'

		if state_id:
			queryset = queryset.filter(STid=state_id)
		else:
			if approved.lower() == 'true':
				in_filter.append('1')
			if denied.lower() == 'true':
				in_filter.append('2')
			if pending.lower() == 'true':
				in_filter.append('3')
			queryset = queryset.filter(STid__in=in_filter)

		return queryset


# Questions
class QuestionSerializer(serializers.ModelSerializer):
	Cname = serializers.SlugRelatedField(source='Cid', read_only=True, slug_field='Cname')

	class Meta:
		model = Question
		fields = ['Qid', 'Cid', 'Cname', 'Qtext', 'QTid', 'Qplaycount']


class QuestionView(viewsets.ReadOnlyModelViewSet):
	queryset = Question.objects.all()
	serializer_class = QuestionSerializer

	def get_queryset(self):
		question_id = self.request.query_params.get('qid')
		category_id = self.request.query_params.get('cid')
		single = self.request.query_params.get('single')
		approved = self.request.query_params.get('approved')
		denied = self.request.query_params.get('denied')
		pending = self.request.query_params.get('pending')
		in_filter = []
		if approved is None:
			approved = 'true'

		if denied is None:
			denied = 'false'

		if pending is None:
			pending = 'false'
		if approved.lower() == 'true':
			in_filter.append('1')
		if denied.lower() == 'true':
			in_filter.append('2')
		if pending.lower() == 'true':
			in_filter.append('3')
		if question_id:
			# Return single question
			queryset = Question.objects.filter(Qid=question_id)
			if len(queryset) < 1:
				return Question.objects.none()
			return queryset

		if category_id:

			if single:
				filter = ['1', '2', '3']
				queryset = Question.objects.all().filter(Q(QTid__in=filter) & Q(Cid=category_id) & Q(STid__in=in_filter))
			else:
				queryset = Question.objects.filter(Q(Cid=category_id) & Q(STid__in=in_filter))
			if len(queryset) < 1:
				return Question.objects.none()
			return queryset

		return Question.objects.none()


class QuestionTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = QuestionType
		fields = ['QTid', 'QTname', 'QTdescription']


class QuestionTypeView(viewsets.ReadOnlyModelViewSet):
	queryset = QuestionType.objects.filter(~Q(QTid=4))
	serializer_class = QuestionTypeSerializer


# Answer
class AnswerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Answer
		fields = ['Anum', 'Atext']


class AnswerView(viewsets.ReadOnlyModelViewSet):
	queryset = Answer.objects.all()
	serializer_class = AnswerSerializer

	def get_queryset(self):
		question_id = self.request.query_params.get('qid')

		if question_id:
			# Return single question
			queryset = Answer.objects.filter(Qid=question_id)
			if len(queryset) < 2:
				return Answer.objects.none()
			return queryset

		return Answer.objects.none()
