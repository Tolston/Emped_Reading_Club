# Generated by Django 3.1.7 on 2021-04-10 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Emped_booksite', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='Age',
        ),
        migrations.DeleteModel(
            name='Range',
        ),
    ]