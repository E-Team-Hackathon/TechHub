from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, get_backends
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

            backend = get_backends()[0]  # 最初の認証バックエンドを取得
            user.backend = f"{backend.__module__}.{backend.__class__.__name__}"

            login(self.request, user) 
            messages.success(self.request, 'アカウントが作成されました！')
            
            self.object = user
            return redirect(self.get_success_url())
        
        except Exception as e:
            form.add_error(None, f'登録中にエラーが発生しました: {str(e)}') 
            return self.form_invalid(form)
        
class CustomLoginView(LoginView):
    def form_valid(self, form):
        username = self.request.POST.get("username")
        password = self.request.POST.get("password")
        user = authenticate(self.request, username=username, password=password)

        if user is None:
            messages.error(self.request, "ログイン情報が間違っています")
            return self.form_invalid(form)

        backend = get_backends()[0]
        user.backend = f"{backend.__module__}.{backend.__class__.__name__}"

        login(self.request, user)
        messages.success(self.request, f"{user.username} さん、ようこそ！")

        return redirect(self.get_success_url())

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

    if request.method == 'POST':
        form = ContributorForm(request.POST)
        if form.is_valid():
            try:
                contributor = form.save(commit=False)
                contributor.user = user  
                contributor.save()
                messages.success(request, "投稿者登録が完了しました！")
                return redirect("mypage") 
            except Exception as e :
                form.add_error(None, "このサイトとアカウント名の組み合わせは既に登録されています")
    else:
        form = ContributorForm() 

    return render(request, 'mypage.html', {
        'user': user,
        'contributors': contributors,
        'articles': articles,
        'favorite_articles':favorite_articles,
        'form': form
    })
