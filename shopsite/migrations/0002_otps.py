# Generated by Django 3.2.8 on 2021-12-09 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopsite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTPs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otpcurrent', models.TextField()),
                ('emailotp', models.CharField(max_length=200)),
            ],
        ),
    ]