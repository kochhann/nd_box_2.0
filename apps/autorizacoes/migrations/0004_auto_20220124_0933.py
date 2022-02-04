# Generated by Django 3.2.10 on 2022-01-24 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autorizacoes', '0003_enturmacao_unidade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluno',
            name='gv_code',
            field=models.IntegerField(unique=True, verbose_name='GV Code'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='matricula',
            field=models.IntegerField(unique=True, verbose_name='Matrícula'),
        ),
        migrations.AlterField(
            model_name='autorizador',
            name='gv_code',
            field=models.IntegerField(unique=True, verbose_name='GV Code'),
        ),
    ]
