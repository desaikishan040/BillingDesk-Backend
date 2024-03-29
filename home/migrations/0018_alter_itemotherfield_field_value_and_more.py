# Generated by Django 4.1.4 on 2023-04-12 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_alter_items_created_by_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemotherfield',
            name='field_value',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='itemotherfield',
            name='parent_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_item', to='home.items'),
        ),
    ]
