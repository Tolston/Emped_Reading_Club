# Generated by Django 3.1.7 on 2021-04-11 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Emped_booksite', '0006_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='Author',
        ),
        migrations.AddField(
            model_name='book',
            name='Author',
            field=models.ManyToManyField(help_text='Select a author of this book', to='Emped_booksite.Author'),
        ),
    ]
