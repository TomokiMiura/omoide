# Generated by Django 3.2 on 2021-05-25 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20210522_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='omoidetran',
            name='posttime',
            field=models.DateField(blank=True, null=True, verbose_name='投稿日時'),
        ),
    ]