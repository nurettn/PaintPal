# Generated by Django 3.1.2 on 2020-11-27 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
