# Generated by Django 4.0.2 on 2022-04-17 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0009_alter_series_cover'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chapter',
            options={'ordering': ['chap']},
        ),
    ]
