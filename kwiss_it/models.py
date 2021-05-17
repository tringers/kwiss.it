from django.db import models
from django.contrib.auth.models import AbstractBaseUser


# Create your models here.
class Picture(models.Model):
	Pid = models.PositiveIntegerField(primary_key=True)
	Pdescription = models.CharField(max_length=256, null=True, blank=True)
	Pcontent = models.CharField(max_length=64)


class User(AbstractBaseUser):
	Uname = models.CharField(max_length=64, unique=True)
	Uemail = models.CharField(max_length=320, unique=True)
	Pid = models.ForeignKey(Picture, null=True, blank=True, on_delete=models.SET_NULL)

	USERNAME_FIELD = 'Uname'
	EMAIL_FIELD = 'Uemail'
	REQUIRED_FIELDS = ['Uname', 'Uemail']


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
	STid = models.ForeignKey(State, db_index=True, default=0, on_delete=models.RESTRICT)
	Cupvotes = models.PositiveIntegerField(db_index=True, default=0)
	Cdownvotes = models.PositiveIntegerField(db_index=True, default=0)


class Score_Category(models.Model):
	Sid = models.ForeignKey(Score, on_delete=models.CASCADE)
	Cid = models.ForeignKey(Category, on_delete=models.CASCADE)
	SCplaycount = models.PositiveIntegerField(default=0)

	class Meta:
		unique_together = ('Sid', 'Cid')


class QuestionType(models.Model):
	QTid = models.PositiveIntegerField(primary_key=True)
	QTdescription = models.CharField(max_length=256)


class Question(models.Model):
	Qid = models.PositiveIntegerField(primary_key=True)
	Cid = models.ForeignKey(Category, db_index=True, default=0, on_delete=models.SET_DEFAULT)
	Pid = models.ForeignKey(Picture, null=True, blank=True, on_delete=models.SET_NULL)
	Qtext = models.CharField(max_length=256)
	STid = models.ForeignKey(State, db_index=True, default=0, on_delete=models.RESTRICT)
	QTid = models.ForeignKey(QuestionType, db_index=True, on_delete=models.RESTRICT)
	Qupvotes = models.PositiveIntegerField(default=0)
	Qdownvotes = models.PositiveIntegerField(default=0)


class Answer(models.Model):
	Qid = models.ForeignKey(Question, on_delete=models.CASCADE)
	Anum = models.PositiveIntegerField()
	Atext = models.CharField(max_length=64)
	Acorrect = models.BooleanField(default=0)

	class Meta:
		unique_together = ('Qid', 'Anum')


class ReportType(models.Model):
	RTid = models.IntegerField(primary_key=True)
	RTname = models.CharField(max_length=32, unique=True)
	RTdescription = models.CharField(max_length=256)


class Report(models.Model):
	Rid = models.IntegerField(primary_key=True)
	RTid = models.ForeignKey(ReportType, on_delete=models.RESTRICT, db_index=True)
	RefId = models.IntegerField(db_index=True)

