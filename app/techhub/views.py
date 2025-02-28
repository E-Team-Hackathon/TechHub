from django.conf import settings
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect,render, get_object_or_404
from django.contrib import messages
from .models import Article, Contributor, Favorite, User

class TopPageView(ListView):
    model = Article
    template_name = 'toppage.html' 
    context_object_name = 'articles'
    paginate_by = 10  # 1ページあたりの記事表示数10

    def get_queryset(self):
        return Article.objects.order_by('-posted_at')  # 記事を投稿順に取得
    
    def get_context_data(self, **kwargs): #**kwargsは複数オブジェクトの辞書型データ
        context = super().get_context_data(**kwargs)

        # Contributor テーブルから user に紐づいた情報を取得（重複阻止）
        unique_users = Contributor.objects.select_related('user').values(
            'user_id', 'user__username', 'user__profile_icon').distinct()

        # `profile_icon` にS3のフルURLを設定する
        contributors_list = []
        for user in unique_users:
            user_instance = User.objects.get(id=user['user_id'])  
            profile_icon_url = user_instance.get_profile_icon_url() 
            contributors_list.append({
                'user_id': user['user_id'],
                'username': user['user__username'],
                'profile_icon': profile_icon_url
        })

        context['contributors'] = contributors_list


         # **ログインしている場合、お気に入りの記事を取得**
        if self.request.user.is_authenticated:
            context['favorite_articles'] = Favorite.objects.filter(user=self.request.user).values_list('article_id', flat=True)
        else:
            context['favorite_articles'] = []
        
        return context
    
def article_search(request):
    query = request.GET.get('query')

    if query:
        articles = Article.objects.all().filter(title__icontains=query)
    else:
        articles = Article.objects.all().order_by('-posted_at')

    unique_users = Contributor.objects.select_related('user').values(
            'user_id', 'user__username', 'user__profile_icon').distinct()

    contributors_list = []
    for user in unique_users:
        profile_icon_path = user.get('user__profile_icon')
        if profile_icon_path:
            profile_icon_url = f"{settings.MEDIA_URL}{profile_icon_path}"
        else:
            profile_icon_url = f"{settings.STATIC_URL}img/default_profile.png"

        contributors_list.append({
            'user_id': user['user_id'],
            'username': user['user__username'],
            'profile_icon': profile_icon_url
        })

    if request.user.is_authenticated:
        favorite_articles = Favorite.objects.filter(user=request.user).values_list('article_id', flat=True)
    else:
        favorite_articles = []

    context = {
        'articles': articles,
        'contributors': contributors_list,
        'favorite_articles': favorite_articles,
    }
        
    return render(request, 'toppage.html', context)
    
def contributor_filtering(request, username=None):  # username をURLパスから取得
    if username:
        articles = Article.objects.filter(contributor__user__username__exact=username)  
    else:
        articles = Article.objects.all()  

    return render(request, 'toppage.html', {'articles': articles})

@login_required
def toggle_favorite(request,article_id):
    article = get_object_or_404(Article, id=article_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user,article=article)

    if not created:
        favorite.delete()
        messages.success(request, f'「{article.title}」をお気に入りから削除しました')
    else:
        messages.success(request, f'「{article.title}」をお気に入りに追加しました')
    
    return redirect('mypage') 