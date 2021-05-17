from django.db import models


# Create your models here.
class User(models.Model):
	Uid = models.PositiveIntegerField(primary_key=True)
	Uname = models.CharField(max_length=64, unique=True)
	Uemail = models.CharField(max_length=320, unique=True)
	Rid = models.SmallIntegerField(max_length=4, db_index=True)
	Pid = models.PositiveIntegerField(null=True, blank=True)
	Upwdhash = models.CharField(max_length=1024)


class Role(models.Model):
	Rid = models.PositiveIntegerField(primary_key=True)
	Rdescriptor = models.CharField(max_length=64)


class Score(models.Model):
	Sid = models.PositiveIntegerField(primary_key=True)
	Uid = models.PositiveIntegerField(unique=True)
	Swon = models.PositiveIntegerField(db_index=True, default=0)
	Slost = models.PositiveIntegerField(db_index=True, default=0)


class Score_Category(models.Model):
	Sid = models.PositiveIntegerField(primary_key=True)
	Cid = models.PositiveIntegerField(primary_key=True)
	SCplaycount = models.PositiveIntegerField(default=0)


class Category(models.Model):
	Cid = models.PositiveIntegerField(primary_key=True)
	Cname = models.CharField(max_length=128)
	Cdescription = models.CharField(max_length=512)
	STid = models.SmallIntegerField(max_length=4, db_index=True, default=0)
	Cupvotes = models.PositiveIntegerField(db_index=True, default=0)
	Cdownvotes = models.PositiveIntegerField(db_index=True, default=0)


class Question(models.Model):
	Qid = models.PositiveIntegerField(primary_key=True)
	Cid = models.PositiveIntegerField(db_index=True)
	Pid = models.PositiveIntegerField(null=True, blank=True)
	Qtext = models.CharField(max_length=255)
	Qstate = models.SmallIntegerField(max_length=4, default=0)
	Qtype = models.SmallIntegerField(max_length=4, default=0)
	Qupvotes = models.PositiveIntegerField(default=0)
	Qdownvotes = models.PositiveIntegerField(default=0)


class Answer(models.Model):
	Qid = models.PositiveIntegerField(primary_key=True)
	Anum = models.PositiveIntegerField(primary_key=True)
	Atext = models.CharField(max_length=64)
	Acorrect = models.BooleanField(default=0)


class Picture(models.Model):
	Pid = models.PositiveIntegerField(primary_key=True)
	Pdescription = models.CharField(max_length=256, null=True, blank=True)
	Pcontent = models.CharField(max_length=64)


# TODO: Add reports and report types
