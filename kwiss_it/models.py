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


# TODO: Add QuestionCorrect, QuestionWrong
class Score(models.Model):
	Sid = models.PositiveIntegerField(primary_key=True)
	Uid = models.OneToOneField(User, on_delete=models.CASCADE)
	Swon = models.PositiveIntegerField(db_index=True, default=0)
	Slost = models.PositiveIntegerField(db_index=True, default=0)


class State(models.Model):
	STid = models.PositiveIntegerField(primary_key=True)
	Sdescription = models.CharField(max_length=256)


class Category(models.Model):
	Cid = models.PositiveIntegerField(primary_key=True)
	Cname = models.CharField(max_length=128)
	Cdescription = models.CharField(max_length=512)
	STid = models.ForeignKey(State, db_index=True, default=0, on_delete=models.RESTRICT, help_text="State ID")
	Cupvotes = models.PositiveIntegerField(db_index=True, default=0)
	Cdownvotes = models.PositiveIntegerField(db_index=True, default=0)


# TODO: Statt pro Kategorie auf Playcount pro Frage
class Score_Category(models.Model):
	Sid = models.ForeignKey(Score, on_delete=models.CASCADE, help_text="Score ID")
	Cid = models.ForeignKey(Category, on_delete=models.CASCADE, help_text="Category ID")
	SCplaycount = models.PositiveIntegerField(default=0)

	class Meta:
		unique_together = ('Sid', 'Cid')


class QuestionType(models.Model):
	QTid = models.PositiveIntegerField(primary_key=True)
	QTdescription = models.CharField(max_length=256)


class Question(models.Model):
	Qid = models.PositiveIntegerField(primary_key=True)
	Cid = models.ForeignKey(Category, db_index=True, default=0, on_delete=models.SET_DEFAULT, help_text="Category ID")
	Pid = models.ForeignKey(Picture, null=True, blank=True, on_delete=models.SET_NULL, help_text="Picture ID")
	Qtext = models.CharField(max_length=256)
	STid = models.ForeignKey(State, db_index=True, default=0, on_delete=models.RESTRICT, help_text="State ID")
	QTid = models.ForeignKey(QuestionType, db_index=True, on_delete=models.RESTRICT, help_text="QuestionType ID")
	Qupvotes = models.PositiveIntegerField(default=0)
	Qdownvotes = models.PositiveIntegerField(default=0)


class Answer(models.Model):
	Qid = models.ForeignKey(Question, on_delete=models.CASCADE, help_text="Question ID")
	Anum = models.PositiveIntegerField()
	Atext = models.CharField(max_length=64)
	Acorrect = models.BooleanField(default=0)

	class Meta:
		unique_together = ('Qid', 'Anum')


class ReportType(models.Model):
	RTid = models.PositiveIntegerField(primary_key=True)
	RTname = models.CharField(max_length=32, unique=True)
	RTdescription = models.CharField(max_length=256)


class Report(models.Model):
	Rid = models.PositiveIntegerField(primary_key=True)
	RTid = models.ForeignKey(ReportType, on_delete=models.RESTRICT, db_index=True, help_text="ReportType ID")
	RefId = models.PositiveIntegerField(db_index=True)


class DiscordRole(models.Model):
	DRid = models.PositiveIntegerField(primary_key=True)
	Uid = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
	DRkey = models.CharField(max_length=36, help_text="Generated UUID4", unique=True)
	DiscordName = models.CharField(max_length=256, help_text="User's Discord Name in base64url")
	Deprecated = models.BooleanField(default=False)
