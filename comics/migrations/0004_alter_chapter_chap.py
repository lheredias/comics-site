# Generated by Django 3.2.8 on 2021-12-18 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0003_chapter_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='chap',
            field=models.IntegerField(),
        ),
    ]
