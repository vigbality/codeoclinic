# Generated by Django 4.1 on 2022-11-23 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_results_pnotes'),
    ]

    operations = [
        migrations.AddField(
            model_name='results',
            name='url',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
