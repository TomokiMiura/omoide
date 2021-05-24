# Generated by Django 3.2 on 2021-05-17 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_omoidetran_posttime'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextTran',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posttime', models.DateTimeField(auto_now_add=True, verbose_name='投稿日時')),
                ('text', models.TextField(verbose_name='本文')),
                ('girl_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.girlmaster')),
                ('men_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.menmaster')),
                ('omoide_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.omoidetran')),
            ],
        ),
        migrations.RemoveField(
            model_name='mentexttran',
            name='men_id',
        ),
        migrations.RemoveField(
            model_name='mentexttran',
            name='omoide_id',
        ),
        migrations.DeleteModel(
            name='GirlTextTran',
        ),
        migrations.DeleteModel(
            name='MenTextTran',
        ),
    ]
