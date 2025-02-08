from django.views.generic import ListView
from .models import Article

class TopPageView(ListView):
    model = Article
    template_name = "toppage.html"  # 表示用のテンプレート
    context_object_name = "articles"
    paginate_by = 10  # 1ページあたりの記事表示数10

    def get_queryset(self):
        return Article.objects.order_by('-posted_at')  # 記事を投稿順に取得

