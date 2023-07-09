# Generated by Django 4.2.2 on 2023-06-24 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_round_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='round',
            name='num_winners',
            field=models.IntegerField(blank=True, null=True, verbose_name='Number of winners'),
        ),
        migrations.AlterField(
            model_name='round',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]