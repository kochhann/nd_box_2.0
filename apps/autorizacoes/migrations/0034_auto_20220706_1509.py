# Generated by Django 3.2.10 on 2022-07-06 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autorizacoes', '0033_remove_coordenador_curso'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='gerador',
            field=models.IntegerField(choices=[(1, 'Instituição'), (2, 'Família')], default=1, verbose_name='Gerador'),
        ),
        migrations.AlterField(
            model_name='autorizacoesmodel',
            name='gerador',
            field=models.IntegerField(choices=[(1, 'Instituição'), (2, 'Família')], default=1, verbose_name='Gerador'),
        ),
    ]
