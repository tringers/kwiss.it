# Generated by Django 3.2.3 on 2021-06-02 20:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kwiss_it', '0015_lobby_lplayerready'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lobby',
            name='Lcurrentplayer',
        ),
        migrations.RemoveField(
            model_name='lobby',
            name='Lplayerready',
        ),
        migrations.CreateModel(
            name='LobbyPlayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LPready', models.BooleanField(default=False)),
                ('Lid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kwiss_it.lobby')),
                ('Uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
