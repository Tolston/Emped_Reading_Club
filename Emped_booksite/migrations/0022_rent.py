# Generated by Django 3.2.3 on 2021-05-26 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Emped_booksite', '0021_delete_rent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StartDate', models.DateField(auto_now_add=True, null=True)),
                ('Status', models.CharField(choices=[('Returned', 'Returned'), ('On Rent', 'On Rent')], default='On Rent', max_length=8)),
                ('ReturnedDate', models.DateField(null=True)),
                ('Book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Emped_booksite.book')),
                ('Customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Emped_booksite.customer')),
                ('CustomerAddress', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Emped_booksite.customeraddress')),
            ],
        ),
    ]
