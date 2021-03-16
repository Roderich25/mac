# Generated by Django 3.0.6 on 2021-03-16 01:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaProducto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('actualizacion', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Categoría Producto',
                'verbose_name_plural': 'Categorías Producto',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='tienda')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('disponibilidad', models.BooleanField(default=True)),
                ('categorias', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda.CategoriaProducto')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
            },
        ),
    ]
