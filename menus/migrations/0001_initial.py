# Generated by Django 3.0.9 on 2020-11-16 18:57

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('restaurantes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaOrdering',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CategoriasMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.CharField(max_length=255)),
                ('ordem_categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='menus.CategoriaOrdering')),
                ('restaurante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurantes.Restaurante')),
            ],
            options={
                'unique_together': {('ordem_categoria', 'restaurante')},
            },
        ),
        migrations.CreateModel(
            name='Fornecedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('restaurante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurantes.Restaurante')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredientes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingrediente', models.CharField(max_length=255)),
                ('price', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('restaurante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurantes.Restaurante')),
            ],
        ),
        migrations.CreateModel(
            name='IngredientesItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ingrediente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menus.Ingredientes')),
            ],
        ),
        migrations.CreateModel(
            name='OrdemDeCompra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('fornecedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menus.Fornecedor')),
                ('restaurante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurantes.Restaurante')),
            ],
        ),
        migrations.CreateModel(
            name='OrdemDeCompraItens',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menus.Ingredientes')),
                ('ordem_compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menus.OrdemDeCompra')),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, null=True)),
                ('ativo', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('restaurante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurantes.Restaurante')),
            ],
        ),
        migrations.CreateModel(
            name='Medida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medida', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('restaurante', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurantes.Restaurante')),
            ],
        ),
        migrations.CreateModel(
            name='ItensMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=255)),
                ('descricao', models.CharField(blank=True, max_length=255, null=True)),
                ('code_id', models.UUIDField(default=uuid.uuid4, null=True)),
                ('name_image', models.ImageField(blank=True, null=True, upload_to='menu')),
                ('price', models.FloatField(blank=True, null=True)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cozinha', models.BooleanField(default=False)),
                ('bar', models.BooleanField(default=False)),
                ('praca1', models.BooleanField(default=False)),
                ('praca2', models.BooleanField(default=False)),
                ('praca3', models.BooleanField(default=False)),
                ('praca4', models.BooleanField(default=False)),
                ('ingpraca1a', models.CharField(blank=True, max_length=255, null=True)),
                ('ingpraca1b', models.CharField(blank=True, max_length=255, null=True)),
                ('ingpraca1c', models.CharField(blank=True, max_length=255, null=True)),
                ('ingpraca1d', models.CharField(blank=True, max_length=255, null=True)),
                ('ingpraca2a', models.CharField(blank=True, max_length=255, null=True)),
                ('ingpraca2b', models.CharField(blank=True, max_length=255, null=True)),
                ('ingpraca2c', models.CharField(blank=True, max_length=255, null=True)),
                ('ingpraca2d', models.CharField(blank=True, max_length=255, null=True)),
                ('ingpraca3a', models.CharField(blank=True, max_length=255, null=True)),
                ('ingpraca3b', models.CharField(blank=True, max_length=255, null=True)),
                ('ingpraca3c', models.CharField(blank=True, max_length=255, null=True)),
                ('ingpraca3d', models.CharField(blank=True, max_length=255, null=True)),
                ('ingpraca4a', models.CharField(blank=True, max_length=255, null=True)),
                ('ingpraca4b', models.CharField(blank=True, max_length=255, null=True)),
                ('ingpraca4c', models.CharField(blank=True, max_length=255, null=True)),
                ('ingpraca4d', models.CharField(blank=True, max_length=255, null=True)),
                ('categoria', models.ManyToManyField(to='menus.CategoriasMenu')),
                ('ingredientes', models.ManyToManyField(to='menus.IngredientesItem')),
                ('menus', models.ManyToManyField(related_name='menu', to='menus.Menu')),
                ('restaurante', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurantes.Restaurante')),
            ],
        ),
        migrations.AddField(
            model_name='ingredientesitem',
            name='medida',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='menus.Medida'),
        ),
        migrations.AddField(
            model_name='ingredientesitem',
            name='restaurante',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurantes.Restaurante'),
        ),
    ]