from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User


# Create your models here.
class Picture(models.Model):
	Pid = models.PositiveIntegerField(primary_key=True)
	Pdescription = models.CharField(max_length=256, null=True, blank=True)
	Pcontent = models.CharField(max_length=64)


class UserPrivate(models.Model):
	Uid = models.OneToOneField(User, on_delete=models.CASCADE)
	UPprivate = models.BooleanField(default=False)
	UPregistered = models.BooleanField(default=True)
	UPlastseen = models.BooleanField(default=True)


class UserDescription(models.Model):
	Uid = models.OneToOneField(User, on_delete=models.CASCADE)
	Udescription = models.CharField(max_length=1000)


class UserPicture(models.Model):
	Uid = models.OneToOneField(User, on_delete=models.CASCADE)
	Pid = models.OneToOneField(Picture, default=0, on_delete=models.SET_DEFAULT)


class UserLastSeen(models.Model):
	Uid = models.OneToOneField(User, on_delete=models.CASCADE)
	LastSeen = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.Uid) + ' : ' + self.LastSeen.strftime("%Y-%m-%d %H:%M")


class Score(models.Model):
	Sid = models.BigAutoField(primary_key=True)
	Uid = models.OneToOneField(User, on_delete=models.RESTRICT)
	Swon = models.PositiveIntegerField(db_index=True, default=0)
	Slost = models.PositiveIntegerField(db_index=True, default=0)
	Qcorrect = models.PositiveIntegerField(db_index=True, default=0)
	Qwrong = models.PositiveIntegerField(db_index=True, default=0)


class State(models.Model):
	STid = models.AutoField(primary_key=True)
	Sdescription = models.CharField(max_length=256)

	def __str__(self):
		return self.Sdescription


class Category(models.Model):
	Cid = models.BigAutoField(primary_key=True)
	Uid = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	Cname = models.CharField(max_length=128, unique=True)
	Cdescription = models.CharField(max_length=512)
	STid = models.ForeignKey(State, db_index=True, default=0, on_delete=models.RESTRICT, help_text="State ID")
	Cupvotes = models.PositiveIntegerField(db_index=True, default=0)
	Cdownvotes = models.PositiveIntegerField(db_index=True, default=0)

	def __str__(self):
		return self.Cname


class CategoryVotes(models.Model):
	Cid = models.ForeignKey(Category, on_delete=models.CASCADE)
	Uid = models.ForeignKey(User, on_delete=models.CASCADE)
	vote = models.SmallIntegerField(default=0)

	class Meta:
		unique_together = ('Qid', 'Uid')


class Score_Category(models.Model):
	Sid = models.ForeignKey(Score, on_delete=models.CASCADE, help_text="Score ID")
	Cid = models.ForeignKey(Category, on_delete=models.CASCADE, help_text="Category ID")

	class Meta:
		unique_together = ('Sid', 'Cid')


class QuestionType(models.Model):
	QTid = models.SmallAutoField(primary_key=True)
	QTname = models.CharField(max_length=32)
	QTdescription = models.CharField(max_length=256)

	def __str__(self):
		return self.QTname + ' : ' + self.QTdescription


class Question(models.Model):
	Qid = models.BigAutoField(primary_key=True)
	Cid = models.ForeignKey(Category, db_index=True, default=0, on_delete=models.SET_DEFAULT, help_text="Category ID")
	Uid = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	Pid = models.ForeignKey(Picture, null=True, blank=True, on_delete=models.SET_NULL, help_text="Picture ID")
	Qtext = models.CharField(max_length=256)
	STid = models.ForeignKey(State, db_index=True, default=0, on_delete=models.RESTRICT, help_text="State ID")
	QTid = models.ForeignKey(QuestionType, db_index=True, on_delete=models.RESTRICT, help_text="QuestionType ID")
	Qplaycount = models.PositiveIntegerField(default=0)
	Qupvotes = models.PositiveIntegerField(default=0)
	Qdownvotes = models.PositiveIntegerField(default=0)
	Qmodupvotes = models.PositiveIntegerField(default=0)
	Qmoddownvotes = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.Qtext


class QuestionVotes(models.Model):
	Qid = models.ForeignKey(Question, on_delete=models.CASCADE)
	Uid = models.ForeignKey(User, on_delete=models.CASCADE)
	vote = models.SmallIntegerField(default=0)

	class Meta:
		unique_together = ('Qid', 'Uid')


class Answer(models.Model):
	Qid = models.ForeignKey(Question, on_delete=models.CASCADE, help_text="Question ID")
	Anum = models.SmallIntegerField()
	Atext = models.CharField(max_length=64)
	Acorrect = models.BooleanField(default=0)

	def __str__(self):
		correct_star = ''
		if self.Acorrect:
			correct_star = '*'

		return str(self.Qid) + ' : ' + correct_star + self.Atext

	class Meta:
		unique_together = ('Qid', 'Anum')


class LobbyType(models.Model):
	LTid = models.SmallAutoField(primary_key=True)
	LTname = models.CharField(max_length=32)
	LTdescription = models.CharField(max_length=1000)

	def __str__(self):
		return self.LTdescription


class Lobby(models.Model):
	Lid = models.BigAutoField(primary_key=True)
	Lkey = models.CharField(max_length=6, unique=True)
	Uid = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	Lname = models.CharField(max_length=64)
	Ltype = models.ForeignKey(LobbyType, on_delete=models.RESTRICT)
	Lplayerlimit = models.PositiveSmallIntegerField(default=8)
	Lquestionamount = models.PositiveSmallIntegerField(default=20)
	Ltimeamount = models.PositiveSmallIntegerField(default=20)
	Lprivate = models.BooleanField(default=False)
	Lpassword = models.CharField(max_length=128, help_text='250000 iterations of SHA256', null=True)
	Lauthtoken = models.CharField(max_length=64, help_text='Auth token for Link join. Should be contained in link', null=True)
	Lcreated = models.DateTimeField(auto_now=True)
	Lstarted = models.BooleanField(default=False)
	LcurrentQuestion = models.PositiveIntegerField(default=0)
	LcurrentCorrect = models.PositiveSmallIntegerField(default=0)

	def is_public_lobby(self):
		return not self.Lprivate

	def is_private_lobby(self):
		return self.Lprivate and (self.Lpassword is not None and self.Lpassword != '')

	def is_solo_lobby(self):
		return self.Lprivate and (self.Lpassword is None or self.Lpassword == '')

	def is_full(self):
		lobbyuser_objset = LobbyUser.objects.filter(Lid=self)
		return self.Lplayerlimit <= len(lobbyuser_objset)

	def check_password(self, password):
		if not password:
			return False
		return self.Lpassword == password

	def check_authtoken(self, authtoken):
		if not authtoken:
			return False
		return self.Lauthtoken == authtoken

	def __str__(self):
		return self.Lname


# Player joining lobby -> currentplayer +1 -> load questions
# Player leaving lobby/or timeout -> currentplayer -1 - unload questions
# All player ready -> wait 5 seconds -> switch to game
# After finished -> play again creates new lobby with same settings -> old lobby currentplayer set 0
# New lobby keep old Uid
# Remove old lobby if a new lobby is created or all player left/timeout


class LobbyCategory(models.Model):
	Lid = models.ForeignKey(Lobby, on_delete=models.CASCADE)
	Cid = models.ForeignKey(Category, on_delete=models.CASCADE)

	class Meta:
		unique_together = ('Lid', 'Cid')


class LobbyUser(models.Model):
	Lid = models.ForeignKey(Lobby, on_delete=models.CASCADE)
	Uid = models.ForeignKey(User, on_delete=models.CASCADE)
	LPready = models.BooleanField(default=False)
	LPLastHeartbeat = models.DateTimeField(auto_now_add=True)
	LPScore = models.IntegerField(default=0)
	LPStreak = models.IntegerField(default=1)
	LPlastaddition = models.IntegerField(default=0)


class LobbyQuestions(models.Model):
	LQid = models.BigAutoField(primary_key=True)
	Lid = models.ForeignKey(Lobby, on_delete=models.CASCADE)
	Qid = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)

	class Meta:
		unique_together = ('Lid', 'Qid')


class ReportType(models.Model):
	RTid = models.SmallAutoField(primary_key=True)
	RTname = models.CharField(max_length=32, unique=True)
	RTdescription = models.CharField(max_length=256)

	def __str__(self):
		return self.RTname + ' : ' + self.RTdescription


class Report(models.Model):
	Rid = models.BigAutoField(primary_key=True)
	RTid = models.ForeignKey(ReportType, on_delete=models.RESTRICT, db_index=True, help_text="ReportType ID")
	RefId = models.PositiveIntegerField(db_index=True)
	Rdescription = models.CharField(max_length=1000, null=True)

	def __str__(self):
		return str(self.Rid) + ' : ' + self.Rdescription


class DiscordRole(models.Model):
	DRid = models.BigAutoField(primary_key=True)
	Uid = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
	DRkey = models.CharField(max_length=36, help_text="Generated UUID4", unique=True)
	DiscordName = models.CharField(max_length=256, help_text="User's Discord Name in base64url")
	Deprecated = models.BooleanField(default=False)

	def __str__(self):
		return str(self.Uid) + ' : ' + self.DiscordName
