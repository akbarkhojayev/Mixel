# Generated by Django 5.2 on 2025-04-22 13:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_galary_options_galary_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='galary',
            name='product',
        ),
        migrations.AddField(
            model_name='product',
            name='galary',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.galary'),
            preserve_default=False,
        ),
    ]
