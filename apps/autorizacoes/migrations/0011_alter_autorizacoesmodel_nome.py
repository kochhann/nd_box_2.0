# Generated by Django 3.2.10 on 2022-02-03 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autorizacoes', '0010_auto_20220203_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autorizacoesmodel',
            name='nome',
            field=models.CharField(max_length=100, verbose_name='Nome'),
        ),
    ]