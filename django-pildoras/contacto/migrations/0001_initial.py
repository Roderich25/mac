# Generated by Django 3.0.6 on 2021-03-15 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contacto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=128)),
                ('email', models.CharField(max_length=128)),
                ('contenido', models.TextField()),
                ('fecha', models.DateField()),
            ],
        ),
    ]
