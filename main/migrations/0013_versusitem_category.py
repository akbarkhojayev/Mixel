# Generated by Django 5.2 on 2025-04-30 08:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_product_galary'),
    ]

    operations = [
        migrations.AddField(
            model_name='versusitem',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.category'),
        ),
    ]
