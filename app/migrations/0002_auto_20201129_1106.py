# Generated by Django 3.1.3 on 2020-11-29 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='title',
            field=models.CharField(max_length=256, unique=True, verbose_name='title'),
        ),
    ]