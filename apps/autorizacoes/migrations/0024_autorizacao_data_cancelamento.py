# Generated by Django 3.2.10 on 2022-04-04 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autorizacoes', '0023_auto_20220331_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='autorizacao',
            name='data_cancelamento',
            field=models.DateField(blank=True, null=True, verbose_name='Data Cancelamento'),
        ),
    ]
