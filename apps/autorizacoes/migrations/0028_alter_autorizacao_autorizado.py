# Generated by Django 3.2.10 on 2022-04-12 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autorizacoes', '0027_auto_20220412_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autorizacao',
            name='autorizado',
            field=models.BooleanField(blank=True, default=None, null=True, verbose_name='Autorização'),
        ),
    ]
