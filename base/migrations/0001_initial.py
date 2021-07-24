# Generated by Django 3.2 on 2021-07-24 05:27

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CoupleMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('girl_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='女性のユーザーID')),
                ('men_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='男性のユーザーID', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OmoideTran',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='タイトル')),
                ('posttime', models.DateField(blank=True, null=True, verbose_name='投稿日時')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='thumbnail/%Y/%m/%d/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'png'])], verbose_name='サムネイル')),
                ('couple_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.couplemaster')),
            ],
        ),
        migrations.CreateModel(
            name='TextTran',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posttime', models.DateTimeField(auto_now_add=True, verbose_name='投稿日時')),
                ('text', models.TextField(blank=True, null=True, verbose_name='コメント')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'png'])], verbose_name='画像')),
                ('author_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('omoide_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.omoidetran')),
            ],
        ),
    ]
