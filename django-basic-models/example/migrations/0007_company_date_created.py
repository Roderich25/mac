# Generated by Django 2.2.6 on 2019-10-17 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('example', '0006_auto_20191017_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='date_created',
            field=models.DateField(null=True),
        ),
    ]
