# Generated by Django 3.2.10 on 2022-04-11 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autorizacoes', '0024_autorizacao_data_cancelamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='autorizacao',
            name='data_resposta_titular',
            field=models.DateField(blank=True, null=True, verbose_name='Data Resposta'),
        ),
        migrations.AlterField(
            model_name='autorizacao',
            name='autorizado',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Autorização'),
        ),
    ]
