# Generated by Django 4.1 on 2022-11-23 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_results_demail_results_page_results_pcontact_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='results',
            name='pNotes',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]