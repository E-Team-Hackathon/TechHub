from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms.signup import SignUpForm
from techhub.models import Article, Contributor
from .forms.contributor import ContributorForm  

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("mypage")
    template_name = "accounts/signup.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        return redirect(self.get_success_url())

@login_required
def profile(request):
    user = request.user
    contributors = Contributor.objects.filter(user=user)

    if request.method == 'POST':
        form = ContributorForm(request.POST)
        if form.is_valid():
            contributor = form.save(commit=False)
            contributor.user = user
            contributor.save()
            return redirect('mypage')
    else:
        form = ContributorForm()

    return render(request,'accounts/profile.html',{'form': form, 'contributors': contributors})

@login_required
def mypage(request):
    user = request.user
    contributors = Contributor.objects.filter(user=user)  # ユーザーの登録したフィード情報
    articles = Article.objects.all().order_by('-posted_at')  # 記事一覧（新着順）

    return render(request, 'accounts/mypage.html', {
        'user': user,
        'contributors': contributors,
        'articles': articles,
    })