# Generated by Django 2.2.4 on 2019-10-25 15:11

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='tutorial_published',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 25, 15, 11, 38, 664711, tzinfo=utc), verbose_name='date published'),
        ),
    ]
