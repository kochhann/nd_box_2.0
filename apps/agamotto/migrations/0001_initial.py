# Generated by Django 3.2.10 on 2022-01-20 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduledTask',
            fields=[
                ('data_criacao', models.DateField(auto_now_add=True, verbose_name='Criação')),
                ('data_modificacao', models.DateField(auto_now=True, verbose_name='Modificação')),
                ('data_desativado', models.DateField(blank=True, default=None, null=True, verbose_name='Desativado')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('task', models.CharField(max_length=100, verbose_name='Tarefa')),
                ('status', models.CharField(max_length=100, verbose_name='Status')),
                ('gv_code', models.IntegerField(blank=True, null=True, verbose_name='GV Code')),
                ('extra_field', models.CharField(blank=True, max_length=200, null=True, verbose_name='Extra')),
                ('error_message', models.CharField(blank=True, max_length=500, null=True, verbose_name='Erro')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
