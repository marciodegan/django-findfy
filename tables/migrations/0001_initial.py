# Generated by Django 3.0.9 on 2020-11-16 18:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurantes', '0001_initial'),
        ('menus', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormaDePagamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forma_pagamento', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('restaurante', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='restaurantes.Restaurante')),
            ],
        ),
        migrations.CreateModel(
            name='Number',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_code', models.CharField(max_length=255)),
                ('qr_code', models.ImageField(blank=True, upload_to='qr_codes')),
                ('table_check_number', models.UUIDField(default=uuid.uuid4, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('pagamento_solicitado', models.BooleanField(default=False)),
                ('pagamento_solicitado_code', models.IntegerField(null=True)),
                ('garcom_confirmado_pagamento', models.BooleanField(default=False)),
                ('chamar_atendente', models.BooleanField(default=False, null=True)),
                ('atendente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('atendentes', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurantes.AtendentesRestaurante')),
                ('restaurante', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurantes.Restaurante')),
            ],
        ),
        migrations.CreateModel(
            name='ValoresCaixa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('forma_pagamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.FormaDePagamento')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.Table')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='caixauser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TableUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('visible', models.BooleanField(default=False, null=True)),
                ('communicate', models.BooleanField(default=False, null=True)),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.Table')),
                ('table_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TableNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_number', models.IntegerField()),
                ('table_ref', models.UUIDField(default=uuid.uuid4)),
                ('openstatus', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('restaurante', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurantes.Restaurante')),
            ],
            options={
                'unique_together': {('table_number', 'restaurante')},
            },
        ),
        migrations.CreateModel(
            name='TableItens',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('order_obs', models.CharField(max_length=144, null=True)),
                ('price', models.FloatField(null=True)),
                ('confirmed', models.BooleanField(default=False)),
                ('garconconfirmed', models.BooleanField(default=False)),
                ('garcon_to_bar', models.BooleanField(default=False)),
                ('bar_to_garcon', models.BooleanField(default=False)),
                ('garcon_to_cozinha', models.BooleanField(default=False)),
                ('cozinha_to_garcon', models.BooleanField(default=False)),
                ('praca1_aceite', models.BooleanField(default=False)),
                ('praca1_entrega', models.BooleanField(default=False)),
                ('praca2_aceite', models.BooleanField(default=False)),
                ('praca2_entrega', models.BooleanField(default=False)),
                ('praca3_aceite', models.BooleanField(default=False)),
                ('praca3_entrega', models.BooleanField(default=False)),
                ('praca4_aceite', models.BooleanField(default=False)),
                ('praca4_entrega', models.BooleanField(default=False)),
                ('item_code', models.IntegerField(null=True)),
                ('atendente_insert', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='atendenteuser', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menus.ItensMenu')),
                ('item_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='itemuser', to=settings.AUTH_USER_MODEL)),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.Table')),
                ('who_confirmed', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='whoconfirmed', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='table',
            name='table_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.TableNumber'),
        ),
        migrations.CreateModel(
            name='Caixa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('caixa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='caixa', to=settings.AUTH_USER_MODEL)),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.Table')),
            ],
        ),
    ]
