# Generated by Django 4.1.7 on 2023-02-28 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_remove_company_hotel_main_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='hotel_Main_Img',
            field=models.ImageField(default=1, upload_to='images/'),
            preserve_default=False,
        ),
    ]
