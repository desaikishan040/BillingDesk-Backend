# Generated by Django 4.1.4 on 2023-04-28 08:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0003_proposal_ask_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]