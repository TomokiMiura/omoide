from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self,email, password, **extra_fields):
        """ユーザーネーム、メールアドレス、パスワードでユーザーを作成・保存"""
        if not email:
            raise ValueError('メールアドレスを入力してください')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_men_user(self,email, password=None, **extra_fields):
        """
        メールアドレス、パスワードで男性ユーザーの情報を作成し、保存する
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_girl_user(self,email, password=None, **extra_fields):
        """
        メールアドレス、パスワードを入力した女性ユーザーの情報を作成し、保存する
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_men', False)
        extra_fields.setdefault('is_girl', True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self,email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    """Django標準のUserをベースにカスタマイズしたUserクラス"""

    class Meta(AbstractUser.Meta):
        db_table = 'user'

    username = models.CharField(
        'ユーザー名',
        max_length=30,
        blank=True,
        null=True,
        validators=[AbstractUser.username_validator],
    )

    email = models.EmailField(
        'メールアドレス',
        unique=True,
        help_text='',
        blank=False
    )
    is_men = models.BooleanField(
        '君は男の子？',
        default=True
    )
    is_girl = models.BooleanField(
        '君は女の子？',
        default=False
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def clean(self):
        """Eメールアドレスの正規化を行う"""
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """特定のユーザーにメールを送る"""
        send_mail(subject, message, from_email, [self.email], **kwargs)