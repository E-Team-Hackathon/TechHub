from django import forms
from techhub.models import Contributor, Feed

class ContributorForm(forms.ModelForm):
    feed = forms.ModelChoiceField(
        queryset=Feed.objects.all(),
        empty_label = '選択してください',
        label = '投稿しているサイト',
    )
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['feed'].label_from_instance = lambda obj: obj.feed_name  # `feed_name` を表示

    class Meta:
        model = Contributor
        fields = ['feed', 'account_name']  # user はログインユーザーから設定されるので不要
