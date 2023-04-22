# Generated by Django 4.1.4 on 2023-04-21 06:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0018_alter_itemotherfield_field_value_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.company')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.items')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
