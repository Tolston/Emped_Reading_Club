# Generated by Django 3.2 on 2021-06-26 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Emped_booksite', '0022_rent'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='IsWishList',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='rent',
            name='ReturnedDate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
