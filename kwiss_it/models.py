from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User


# Create your models here.
class Picture(models.Model):
	Pid = models.PositiveIntegerField(primary_key=True)
	Pdescription = models.CharField(max_length=256, null=True, blank=True)
	Pcontent = models.CharField(max_length=64)


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


##TODO Zuordnung Kategorie/Fragen zu User, für Bearbeitung durch diesen
class Category(models.Model):
	Cid = models.BigAutoField(primary_key=True)
	Cname = models.CharField(max_length=128)
	Cdescription = models.CharField(max_length=512)
	STid = models.ForeignKey(State, db_index=True, default=0, on_delete=models.RESTRICT, help_text="State ID")
	Cupvotes = models.PositiveIntegerField(db_index=True, default=0)
	Cdownvotes = models.PositiveIntegerField(db_index=True, default=0)


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
	Pid = models.ForeignKey(Picture, null=True, blank=True, on_delete=models.SET_NULL, help_text="Picture ID")
	Qtext = models.CharField(max_length=256)
	STid = models.ForeignKey(State, db_index=True, default=0, on_delete=models.RESTRICT, help_text="State ID")
	QTid = models.ForeignKey(QuestionType, db_index=True, on_delete=models.RESTRICT, help_text="QuestionType ID")
	Qplaycount = models.PositiveIntegerField(default=0)
	Qupvotes = models.PositiveIntegerField(default=0)
	Qdownvotes = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.Qtext


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


##TODO Lobbys
class LobbyType(models.Model):
	LTid = models.SmallAutoField(primary_key=True)
	LTname = models.CharField(max_length=32)
	LTdescription = models.CharField(max_length=1000)


class Lobby(models.Model):
	Lid = models.BigAutoField(primary_key=True)
	Lname = models.CharField(max_length=64)
	Ltype = models.ForeignKey(LobbyType, on_delete=models.RESTRICT)
	Lprivate = models.BooleanField(default=False)
	Lpassword = models.CharField(max_length=128, help_text='250000 iterations of SHA256')
	Lcreated = models.DateTimeField(auto_now=True)


class Lobby_Player(models.Model):
	Lid = models.ForeignKey(Lobby, on_delete=models.CASCADE)
	Uid = models.ForeignKey(User, on_delete=models.RESTRICT)
	LPwon = models.BooleanField(default=False)


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
