from django import forms
from techhub.models import Contributor, Feed

class ContributorForm(forms.ModelForm):
    feed = forms.ModelChoiceField(
        queryset=Feed.objects.all(),
        empty_label = '選択してください',
        label = '投稿しているサイト',
        widget=forms.RadioSelect
    )
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['feed'].label_from_instance = lambda obj: obj.feed_name  # `feed_name` を表示

    class Meta:
        model = Contributor
        fields = ['feed', 'account_name']  # user はログインユーザーから設定されるので不要

    def clean(self):
        cleaned_data = super().clean()
        feed = cleaned_data.get("feed")
        account_name = cleaned_data.get("account_name")

        # すでに同じ feed と account_name の組み合わせが存在するかチェック
        if Contributor.objects.filter(feed=feed, account_name=account_name).exists():
            raise forms.ValidationError("このサイトとアカウント名の組み合わせは既に登録されています。")

        return cleaned_data

