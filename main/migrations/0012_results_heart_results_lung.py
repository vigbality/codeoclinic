# Generated by Django 4.1 on 2022-11-24 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_remove_results_demail_remove_results_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='results',
            name='heart',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='results',
            name='lung',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
    ]
