from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


# Create your models here.

class UserManager(BaseUserManager):
    """
    Create and save user with email
    """
    use_in_migrations = True

    # def _create_user(self, username, email, password, **extra_fields):
    def _create_user(self,email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        # ユーザー名は必須ではないのでコメントアウト
        # if not username:
        #     raise ValueError('The given username must be set')

        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        # ユーザー名は必須ではないのでコメントアウト
        # username = self.model.normalize_username(username)
        # user = self.model(username=username, email=email, **extra_fields)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # def create_men_user(self, username, email=None, password=None, **extra_fields):
    def create_men_user(self,email, password=None, **extra_fields):
        """
        メールアドレス、パスワードを入力した男性ユーザーの情報を作成し、保存する
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        # return self._create_user(username, email, password, **extra_fields)
        return self._create_user(email, password, **extra_fields)

    # def create_girl_user(self, username, email=None, password=None, **extra_fields):
    def create_girl_user(self,email, password=None, **extra_fields):
        """
        メールアドレス、パスワードを入力した女性ユーザーの情報を作成し、保存する
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        # 男性フラグをOFF
        extra_fields.setdefault('is_men', False)
        # 女性フラグをONf
        extra_fields.setdefault('is_girl', True)
        # return self._create_user(username, email, password, **extra_fields)
        return self._create_user(email, password, **extra_fields)

    # def create_superuser(self, username, email, password, **extra_fields):
    def create_superuser(self,email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # return self._create_user(username, email, password, **extra_fields)
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Django標準のUserをベースにカスタマイズしたUserクラス
    """

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
        default=True,
        # help_text=_(
        #     'Designates whether this user is men.'
        # ),
    )
    is_girl = models.BooleanField(
        '君は女の子？',
        default=False,
        # help_text=_(
        #     'Designates whether this user is girl.'
        # ),
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    # first_nameとlast_nameに関する部分はコメントアウト
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)