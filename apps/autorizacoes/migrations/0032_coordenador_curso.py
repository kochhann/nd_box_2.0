# Generated by Django 3.2.10 on 2022-07-01 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20220124_0933'),
        ('autorizacoes', '0031_alter_autorizacao_evento'),
    ]

    operations = [
        migrations.AddField(
            model_name='coordenador',
            name='curso',
            field=models.ManyToManyField(blank=True, to='core.Curso', verbose_name='Curso'),
        ),
    ]
