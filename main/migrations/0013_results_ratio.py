# Generated by Django 4.1 on 2022-11-24 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_results_heart_results_lung'),
    ]

    operations = [
        migrations.AddField(
            model_name='results',
            name='ratio',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
    ]