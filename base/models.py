from django.db import models
from accounts.models import User
from django.core.validators import FileExtensionValidator

# Create your models here
class CoupleMasterManager(models.Manager):

    pass

class MenMasterManager(models.Manager):

    pass

class GirlMasterManager(models.Manager):

    pass

class OmoideTranManager(models.Manager):

    pass

class TextTranManager(models.Manager):

    pass

class CoupleMaster(models.Model):

    men_id = models.ForeignKey(
        User,
        related_name='men_instance',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    girl_id = models.ForeignKey(
        User,
        related_name='girl_instance',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    objects = CoupleMasterManager()

class OmoideTran(models.Model):

    couple_id = models.ForeignKey(

        CoupleMaster,
        on_delete=models.CASCADE,
        null=False,
        blank=False,

    )

    title = models.CharField(

        verbose_name = 'タイトル',
        max_length=30,
        null=False,
        blank=False,

    )

    posttime = models.DateField(
        
        '投稿日時',
        blank=True,
        null=True,

    )

    thumbnail = models.ImageField(
        verbose_name='サムネイル',
        validators=[FileExtensionValidator(['jpg', 'png'])],
        upload_to='thumbnail/%Y/%m/%d/',
        null=True,
        blank=True,
    )

    objects = OmoideTranManager()

    def __str__(self):
        return self.title

class TextTran(models.Model):

    omoide_id = models.ForeignKey(

        OmoideTran,
        on_delete=models.CASCADE,
        null=False,
        blank=False,

    )

    author_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,

    )

    posttime = models.DateTimeField(
        
        '投稿日時',
        auto_now_add=True,

    )

    text = models.TextField(
        
        verbose_name = 'コメント',
        null=True,
        blank=True,

    )

    image = models.ImageField(
        verbose_name='画像',
        validators=[FileExtensionValidator(['jpg', 'png'])],
        upload_to='images/%Y/%m/%d/',
        null=True,
        blank=True,
    )

    objects = TextTranManager()

    def __str__(self):
        return self.text