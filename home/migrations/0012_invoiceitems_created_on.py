# Generated by Django 4.1.7 on 2023-02-28 13:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_invoiceitems'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceitems',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2023, 2, 28, 13, 59, 39, 653569, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]