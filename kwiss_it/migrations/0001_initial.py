# Generated by Django 3.2.3 on 2021-05-17 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('Cid', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('Cname', models.CharField(max_length=128)),
                ('Cdescription', models.CharField(max_length=512)),
                ('Cupvotes', models.PositiveIntegerField(db_index=True, default=0)),
                ('Cdownvotes', models.PositiveIntegerField(db_index=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('Pid', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('Pdescription', models.CharField(blank=True, max_length=256, null=True)),
                ('Pcontent', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionType',
            fields=[
                ('QTid', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('QTdescription', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='ReportType',
            fields=[
                ('RTid', models.IntegerField(primary_key=True, serialize=False)),
                ('RTname', models.CharField(max_length=32, unique=True)),
                ('RTdescription', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('STid', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('Sdescription', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('Uname', models.CharField(max_length=64, unique=True)),
                ('Uemail', models.CharField(max_length=320, unique=True)),
                ('Pid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='kwiss_it.picture')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('Sid', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('Swon', models.PositiveIntegerField(db_index=True, default=0)),
                ('Slost', models.PositiveIntegerField(db_index=True, default=0)),
                ('Uid', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='kwiss_it.user')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('Rid', models.IntegerField(primary_key=True, serialize=False)),
                ('RefId', models.IntegerField(db_index=True)),
                ('RTid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='kwiss_it.reporttype')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('Qid', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('Qtext', models.CharField(max_length=256)),
                ('Qupvotes', models.PositiveIntegerField(default=0)),
                ('Qdownvotes', models.PositiveIntegerField(default=0)),
                ('Cid', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='kwiss_it.category')),
                ('Pid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='kwiss_it.picture')),
                ('QTid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='kwiss_it.questiontype')),
                ('STid', models.ForeignKey(default=0, on_delete=django.db.models.deletion.RESTRICT, to='kwiss_it.state')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='STid',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.RESTRICT, to='kwiss_it.state'),
        ),
        migrations.CreateModel(
            name='Score_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SCplaycount', models.PositiveIntegerField(default=0)),
                ('Cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kwiss_it.category')),
                ('Sid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kwiss_it.score')),
            ],
            options={
                'unique_together': {('Sid', 'Cid')},
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Anum', models.PositiveIntegerField()),
                ('Atext', models.CharField(max_length=64)),
                ('Acorrect', models.BooleanField(default=0)),
                ('Qid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kwiss_it.question')),
            ],
            options={
                'unique_together': {('Qid', 'Anum')},
            },
        ),
    ]