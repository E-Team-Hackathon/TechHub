from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect,render, get_object_or_404
from django.contrib import messages
from .models import Article, Contributor, Favorite

class TopPageView(ListView):
    model = Article
    template_name = 'toppage.html'  # 表示用のテンプレート
    context_object_name = 'articles'
    paginate_by = 10  # 1ページあたりの記事表示数10

    def get_queryset(self):
        return Article.objects.order_by('-posted_at')  # 記事を投稿順に取得
    
    def get_context_data(self, **kwargs): #**kwargsは複数オブジェクトの辞書型データ
        #ListView の デフォルトのコンテキストデータを取得してsuper（）でさらに新しいオブジェクトを追加するための変数
        context = super().get_context_data(**kwargs)
        # #userとcontributorテーブルをuserカラムをもとに結合。usernameだけを取得
        # unique_users = Contributor.objects.select_related('user').values('user__username').distinct()
        # #辞書型リストのunique_usersをリストに変換
        # context['contributors'] = [user['user__username'] for user in unique_users]
        
        # Contributor テーブルから user に紐づいた情報を取得
        contributors = Contributor.objects.select_related('user').all()

        # ユーザー名とアイコン情報を context に含める
        context['contributors'] = [
            {
                'username': contributor.user.username,
                'profile_icon': contributor.user.profile_icon.url
            }
            for contributor in contributors
        ]

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
    return render(request, 'toppage.html', {'articles':articles})
    
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