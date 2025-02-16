from django.views.generic import ListView
from .models import Article, Contributor

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
        #userとcontributorテーブルをuserカラムをもとに結合。usernameだけを取得
        unique_users = Contributor.objects.select_related('user').values('user__username').distinct()
        #辞書型リストのunique_usersをリストに変換
        context['contributors'] = [user['user__username'] for user in unique_users]
        print('contributors')
        return context