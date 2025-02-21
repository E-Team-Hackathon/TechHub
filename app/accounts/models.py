from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("ユーザー名を入力してください")
        if not password:
            raise ValueError("パスワードを入力してください")
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        unique=True, 
        max_length=255,
        verbose_name='ユーザー名',
        help_text='Mattermost名を入力ください')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # upload_toパラメータで保存先をiconsディレクトリに指定。null=True, blank=Trueは画像の指定がない場合でもエラーをださない設定
    profile_icon = models.ImageField(upload_to="icons", null=False, blank=True, default='icons/default_icon.jpg')

    objects = UserManager()

    #ログインする時にはusernameを使用
    USERNAME_FIELD = 'username'
    # 管理コマンドを使用してスーパーユーザーを作成する際に必要とされるフィールド
    REQUIRED_FIELDS = ['password']

    # 管理者などで区別がつきやすいようにusernameで表示
    def __str__(self):
        return self.username