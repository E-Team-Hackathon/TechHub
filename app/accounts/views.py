from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms.signup import SignUpForm
from techhub.models import Article, Contributor, Favorite
from .forms.contributor import ContributorForm  

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('mypage')
    template_name = 'signup.html'

    def form_valid(self, form):
        try:
            user = form.save(commit=True)

            login(self.request, user) 
            messages.success(self.request, 'アカウントが作成されました！')
            
            self.object = user
            return redirect(self.get_success_url())
        
        except Exception as e:
            form.add_error(None, f'登録中にエラーが発生しました: {str(e)}') 
            return self.form_invalid(form)

@login_required
def profile(request):
    user = request.user
    contributors = Contributor.objects.filter(user=user)

    if request.method == 'POST':
        form = ContributorForm(request.POST)
        if form.is_valid():
            try:
                contributor = form.save(commit=False)
                if Contributor.objects.filter(feed=contributor.feed, account_name=contributor.account_name).exists():
                    form.add_error(None, 'このサイトとアカウント名の組み合わせは既に登録されています')
                else:
                    contributor.user = user
                    contributor.save()
                    return redirect('mypage')
            except Exception:
                form.add_error(None, '登録中にエラーが発生しました:' + str(Exception))
    else:
        form = ContributorForm()

    return render(request,'profile.html',{'form': form, 'contributors': contributors})

@login_required
def mypage(request):
    user = request.user
    contributors = Contributor.objects.filter(user=user)  # ユーザーの登録したフィード情報
    articles = Article.objects.all().order_by('-posted_at')  # 記事一覧（新着順）
    favorite_articles = Favorite.objects.filter(user=user).select_related('article')

    return render(request, 'mypage.html', {
        'user': user,
        'contributors': contributors,
        'articles': articles,
        'favorite_articles':favorite_articles
    })
