# Generated by Django 3.2.8 on 2021-12-25 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0006_series_about'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='about',
            field=models.TextField(default='', max_length=500),
        ),
    ]
