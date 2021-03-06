# Generated by Django 3.2.8 on 2021-12-09 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopsite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnconfirmOrders',
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
                ('item_name', models.CharField(max_length=200)),
                ('orderdate', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='orderdate',
            field=models.DateTimeField(),
        ),
    ]
