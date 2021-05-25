from django.db import models

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
    password = models.CharField(
        verbose_name='パスワード',
        max_length=50,
        null=False,
        blank=False,
    )

    objects = CoupleMasterManager()
    
class MenMaster(models.Model):

    men_mail = models.EmailField(
        
        verbose_name='彼氏のメールアドレス',
        max_length=100,
        null=False,
        blank=False,
    )

    men_nickname = models.CharField(
        verbose_name='彼氏のニックネーム',
        max_length=10,
        null=False,
        blank=False,
    )

    couple_id = models.ForeignKey(

        CoupleMaster,
        verbose_name='カップルID',
        on_delete=models.CASCADE,
        null=False,
        blank=False,

    )

    objects = MenMasterManager()

    def __str__(self):
        return self.men_nickname
    
class GirlMaster(models.Model):

    girl_mail = models.EmailField(
        
        verbose_name='彼女のメールアドレス',
        max_length=100,
        null=False,
        blank=False,

    )
    girl_nickname = models.CharField(

        verbose_name='彼女のニックネーム',
        max_length=10,
        null=False,
        blank=False,
    )

    couple_id = models.ForeignKey(

        CoupleMaster,
        verbose_name='カップルID',
        on_delete=models.CASCADE,
        null=False,
        blank=False,

    )

    objects = GirlMasterManager()

    def __str__(self):
        return self.girl_nickname

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
        null=True

    )

    objects = OmoideTranManager()

    def __str__(self):
        return self.title
    #sumnail_imageはここに追加

#class MenPictureTran(models.Model):
#class GirlPictureTran(models.Model):

class TextTran(models.Model):

    omoide_id = models.ForeignKey(

        OmoideTran,
        on_delete=models.CASCADE,
        null=False,
        blank=False,

    )

    men_id = models.ForeignKey(
        MenMaster,
        on_delete=models.CASCADE,
        null=True,
        blank=True,

    )

    girl_id = models.ForeignKey(
        GirlMaster,
        on_delete=models.CASCADE,
        null=True,
        blank=True,

    )

    posttime = models.DateTimeField(
        
        '投稿日時',
        auto_now_add=True,

    )

    text = models.TextField(

        verbose_name = '本文',
        null=False,
        blank=False,

    )

    objects = TextTranManager()

    def __str__(self):
        return self.text