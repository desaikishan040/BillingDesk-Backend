# Generated by Django 4.1.4 on 2023-03-06 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_alter_company_gst_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='coustomer_mail',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]