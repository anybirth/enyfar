import uuid
import datetime
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.core.mail import send_mail

# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    tel_number_regex = RegexValidator(regex = r'^[0-9]+$', message = ("電話番号はハイフンを除いた半角数字で入力してください。"))

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True, blank=True, null=True)
    phone_number = models.CharField(_('電話番号'), validators=[tel_number_regex], max_length=15, unique=True, blank=True, null=True)
    uuid = models.UUIDField('ユニークID', primary_key=False, blank=True, null=True)
    uuid_deadline = models.DateTimeField(_('ユニークID有効期限'), blank=True, null=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    jender = models.SmallIntegerField(_('性別'), blank=True, null=True)
    birthday = models.DateField(_('生年月日'), blank=True, null=True)
    profession = models.CharField(_('職業'), max_length=50, blank=True)
    line_id = models.CharField(_('LINE ID'), max_length=255, blank=True, null=True, unique=True)
    twitter_id = models.CharField(_('Twitter ID'), max_length=255, blank=True, null=True, unique=True)
    instagram_id = models.CharField(_('Instagram ID'), max_length=255, blank=True, null=True, unique=True)
    facebook_id = models.CharField(_('Facebook ID'), max_length=255, blank=True, null=True, unique=True)
    whatsapp_id = models.CharField(_('WhatsApp ID'), max_length=255, blank=True, null=True, unique=True)
    kik_id = models.CharField(_('KIK ID'), max_length=255, blank=True, null=True, unique=True)
    wechat_id = models.CharField(_('WeChat ID'), max_length=255, blank=True, null=True, unique=True)
    level = models.SmallIntegerField(_('ユーザーレベル'), default=1)
    notice = models.BooleanField(_('配信の希望'), default=False)
    email_verified = models.BooleanField(_('メールアドレス認証'), default=False)
    is_traveller = models.BooleanField(_('トラベラーフラグ'), default=False)
    is_banned = models.BooleanField(_('アカウント凍結'), default=False)
    social_confirm_deadline = models.DateTimeField(_('ソーシャルログイン確認期限'), blank=True, null=True)
    created_at = models.DateTimeField(_('作成日時'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新日時'), auto_now=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

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

class UserAddress(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name=_('ユーザーID'))
    district = models.ForeignKey('meta.District', on_delete=models.CASCADE, verbose_name=_('行政区画ID'))
    postal_code = models.CharField(_('郵便番号'), max_length=9)
    address1 = models.CharField(_('住所1'), max_length=255)
    address2 = models.CharField(_('住所2'), max_length=255, blank=True)
    first_name = models.CharField(_('名'), max_length=50)
    last_name = models.CharField(_('姓'), max_length=50)
    is_default = models.BooleanField(_('デフォルトフラグ'), default=False)
    created_at = models.DateTimeField(_('作成日時'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新日時'), auto_now=True)

    class Meta:
        verbose_name = _('ユーザー住所')
        verbose_name_plural = _('ユーザー住所')

    def __str__(self):
        return '%s' % self.user.username

class Itinerary(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name=_('ユーザーID'))
    purpose = models.SmallIntegerField(_('目的'))
    description = models.TextField(_('備考'), blank=True)
    created_at = models.DateTimeField(_('作成日時'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新日時'), auto_now=True)

    class Meta:
        verbose_name = _('旅程')
        verbose_name_plural = _('旅程')

    def __str__(self):
        return '%s' % self.user.username

class Transfer(models.Model):
    itinerary = models.ForeignKey('Itinerary', on_delete=models.CASCADE, verbose_name=_('旅程ID'))
    departure = models.OneToOneField('Departure', on_delete=models.CASCADE, verbose_name=_('出発ID'))
    arrival = models.OneToOneField('Arrival', on_delete=models.CASCADE, verbose_name=_('到着ID'))
    ticket = models.SmallIntegerField(_('チケット取得状況'))
    created_at = models.DateTimeField(_('作成日時'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新日時'), auto_now=True)

    class Meta:
        verbose_name = _('移動')
        verbose_name_plural = _('移動')

    def __str__(self):
        return '%s' % self.itinerary.user.username

class Flight(models.Model):
    transfer = models.ForeignKey('Transfer', on_delete=models.CASCADE, verbose_name=_('移動ID'))
    flight_number = models.CharField(_('フライトナンバー'), max_length=255)
    created_at = models.DateTimeField(_('作成日時'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新日時'), auto_now=True)

    class Meta:
        verbose_name = _('フライト')
        verbose_name_plural = _('フライト')

    def __str__(self):
        return '%s' % self.flight_number

class Departure(models.Model):
    country = models.OneToOneField('meta.Country', on_delete=models.CASCADE, verbose_name=_('国・地域ID'))
    district = models.OneToOneField('meta.District', on_delete=models.CASCADE, verbose_name=_('行政区画ID'))
    departing_at = models.DateTimeField(_('出発日時'))
    created_at = models.DateTimeField(_('作成日時'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新日時'), auto_now=True)

    class Meta:
        verbose_name = _('出発')
        verbose_name_plural = _('出発')

    def __str__(self):
        return '%s' % self.departing_at

class Arrival(models.Model):
    country = models.OneToOneField('meta.Country', on_delete=models.CASCADE, verbose_name=_('国・地域ID'))
    district = models.OneToOneField('meta.District', on_delete=models.CASCADE, verbose_name=_('行政区画ID'))
    arriving_at  = models.DateTimeField(_('到着日時'))
    created_at = models.DateTimeField(_('作成日時'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新日時'), auto_now=True)

    class Meta:
        verbose_name = _('到着')
        verbose_name_plural = _('到着')

    def __str__(self):
        return '%s' % self.arriving_at
