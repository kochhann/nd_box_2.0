# Generated by Django 3.2.10 on 2022-01-19 19:34

from django.db import migrations, models
import django.db.models.deletion
import functions


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('data_criacao', models.DateField(auto_now_add=True, verbose_name='Criação')),
                ('data_modificacao', models.DateField(auto_now=True, verbose_name='Modificação')),
                ('data_desativado', models.DateField(blank=True, default=None, null=True, verbose_name='Desativado')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=200, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Área de Interesse',
                'verbose_name_plural': 'Áreas de Interesse',
            },
        ),
        migrations.CreateModel(
            name='Escolaridade',
            fields=[
                ('data_criacao', models.DateField(auto_now_add=True, verbose_name='Criação')),
                ('data_modificacao', models.DateField(auto_now=True, verbose_name='Modificação')),
                ('data_desativado', models.DateField(blank=True, default=None, null=True, verbose_name='Desativado')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=200, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Escolaridade',
                'verbose_name_plural': 'Escolaridades',
            },
        ),
        migrations.CreateModel(
            name='Vaga',
            fields=[
                ('data_criacao', models.DateField(auto_now_add=True, verbose_name='Criação')),
                ('data_modificacao', models.DateField(auto_now=True, verbose_name='Modificação')),
                ('data_desativado', models.DateField(blank=True, default=None, null=True, verbose_name='Desativado')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cod_vaga', models.CharField(max_length=200, verbose_name='Código')),
                ('titulo', models.CharField(max_length=200, verbose_name='Título')),
                ('descricao', models.TextField(max_length=300, verbose_name='Descrição')),
                ('tempo_experiencia', models.CharField(max_length=200, verbose_name='Tempo de experiência')),
                ('preenchida', models.BooleanField(default=False, verbose_name='Preenchida')),
                ('area_interesse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='carreiras.area', verbose_name='Área de interesse')),
                ('escolaridade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='carreiras.escolaridade', verbose_name='Escolaridade')),
                ('unidade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.unidade', verbose_name='Unidade')),
            ],
            options={
                'verbose_name': 'Vaga',
                'verbose_name_plural': 'Vagas',
            },
        ),
        migrations.CreateModel(
            name='Candidatura',
            fields=[
                ('data_criacao', models.DateField(auto_now_add=True, verbose_name='Criação')),
                ('data_modificacao', models.DateField(auto_now=True, verbose_name='Modificação')),
                ('data_desativado', models.DateField(blank=True, default=None, null=True, verbose_name='Desativado')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=200, verbose_name='Nome')),
                ('email', models.CharField(max_length=200, verbose_name='E-mail')),
                ('cidade', models.CharField(default='Canoas', max_length=200, verbose_name='Cidade')),
                ('telefone', models.CharField(max_length=15, verbose_name='Telefone')),
                ('curso', models.CharField(blank=True, max_length=15, null=True, verbose_name='Curso')),
                ('historico', models.TextField(blank=True, max_length=300, null=True, verbose_name='Pós-graduação')),
                ('tempo_experiencia', models.CharField(blank=True, max_length=100, null=True, verbose_name='')),
                ('arquivo', models.FileField(upload_to=functions.get_file_path)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('area_interesse', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='carreiras.area', verbose_name='Área de interesse')),
                ('cod_vaga', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='carreiras.vaga', verbose_name='Vaga')),
                ('escolaridade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='carreiras.escolaridade', verbose_name='Escolaridade')),
                ('unidade_interesse', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.unidade', verbose_name='Unidade de interesse')),
            ],
            options={
                'verbose_name': 'Candidatura',
                'verbose_name_plural': 'Candidaturas',
            },
        ),
    ]
