# Generated by Django 2.2.13 on 2020-06-14 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
