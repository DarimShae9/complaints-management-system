# Generated by Django 4.2.3 on 2023-08-01 19:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0014_remove_product_company_alter_message_creation_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 1, 19, 37, 42, 75157)),
        ),
        migrations.AlterField(
            model_name='order',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 1, 19, 37, 42, 74251)),
        ),
        migrations.AlterField(
            model_name='order',
            name='modification_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 1, 19, 37, 42, 74266)),
        ),
    ]
