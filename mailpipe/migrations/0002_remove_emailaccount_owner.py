# Generated by Django 2.2 on 2019-04-10 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailpipe', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailaccount',
            name='owner',
        ),
    ]
