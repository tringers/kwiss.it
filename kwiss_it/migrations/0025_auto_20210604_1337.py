# Generated by Django 3.2.3 on 2021-06-04 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kwiss_it', '0024_auto_20210604_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testtest',
            name='Did',
            field=models.ForeignKey(on_delete=models.CASCADE, to='kwiss_it.discordrole'),
        ),
        migrations.AlterField(
            model_name='testtest',
            name='Lid',
            field=models.ForeignKey(on_delete=models.CASCADE, to='kwiss_it.lobby'),
        ),
    ]