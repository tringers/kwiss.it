from django.db.models import Q
from .models import LobbyType, Lobby, LobbyPlayer, Category, QuestionType, Question, Answer
from rest_framework import routers, serializers, viewsets

#class LobbyTypeSerializer(serializers.ModelSerializer):
#	class Meta:
#		model = LobbyType
#		fields = ['']

class LobbySerializer(serializers.ModelSerializer):
	class Meta:
		model = Lobby
		fields = ['Lkey', 'Lname', 'Ltype', 'Lplayerlimit', 'Lprivate']

class LobbyView(viewsets.ReadOnlyModelViewSet):
	queryset = Lobby.objects.filter(Lstarted=False)
	serializer_class = LobbySerializer

	def get_queryset(self):
		#time = self.request.query_params.get('time')
		queryset = Lobby.objects.filter(
			Q(Lstarted=False) &
			(
				Q(Lprivate=True) &
				Q(Lpassword__isnull=False) |
				Q(Lprivate=False)
			)
		)

		return queryset




