# Generated by Django 4.1.4 on 2023-04-12 06:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0015_rename_profit_amount_expanse_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='created_by_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ItemOtherfield',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_type', models.CharField(choices=[('number', 'NUMBER'), ('text', 'TEXT'), ('checkbox', 'CHECKBOX')], default='text', max_length=10)),
                ('field_name', models.TextField(max_length=50)),
                ('field_value', models.TextField(max_length=500)),
                ('parent_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.items')),
            ],
        ),
    ]
