# Generated by Django 3.2.10 on 2022-03-24 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autorizacoes', '0019_auto_20220323_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='data_termino',
            field=models.DateField(default='2021-01-01', verbose_name='Data Término'),
            preserve_default=False,
        ),
    ]
