from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

User = get_user_model()


class SignUpForm(UserCreationForm):
    usable_password = None
    profile_icon = forms.ImageField(required=False)  # アイコンは任意（アップロードしなくてもOK）

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', "profile_icon") # icon を追加
