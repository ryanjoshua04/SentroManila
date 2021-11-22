# Generated by Django 3.2.8 on 2021-11-21 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopsite', '0002_auto_20211120_1954'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('email_address', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=500)),
                ('message', models.TextField()),
                ('quantity', models.BigIntegerField()),
                ('contact_number', models.BigIntegerField()),
                ('order_itemid', models.IntegerField()),
                ('orderdate', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]