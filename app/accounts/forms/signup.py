import re, unicodedata
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms


User = get_user_model()

class SignUpForm(UserCreationForm):
    usable_password = None
    profile_icon = forms.ImageField(
        required=False,
        label='ユーザーアイコン',
    )  # アイコンは任意（アップロードしなくてもOK）

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', "profile_icon") # icon を追加

    def clean_username(self):
        #ユーザー名は日本語と英数字,@,_,-のみ許可
        username = self.cleaned_data.get("username")

        normalized_username = unicodedata.normalize('NFKC', username)

        if not re.match(r'^[a-zA-Z0-9ぁ-んァ-ヶ一-龠々ー@._-]+$', normalized_username):
            raise forms.ValidationError('ユーザー名はMattermost名と同じにするのを推奨します')
        return username

    def clean_password2(self):
        #パスワードの一致を確認
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("パスワードが一致しません。")
        return password2

    def save(self, commit=True):
        #ユーザーを作成
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"]) 
        if commit:
            user.save()
        return user