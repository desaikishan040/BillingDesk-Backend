# Generated by Django 4.1.7 on 2023-03-05 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_remove_company_gst_regitered'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='coustomer_mail',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]