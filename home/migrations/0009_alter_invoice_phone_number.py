# Generated by Django 4.1.4 on 2023-03-09 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_invoice_customer_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='Phone_number',
            field=models.CharField(blank=True, max_length=13),
        ),
    ]
