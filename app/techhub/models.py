from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Feed(models.Model):
    feed_url = models.URLField(max_length=255)
    feed_name = models.CharField(max_length=255)  

class Contributor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed,on_delete=models.CASCADE)
    account_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['feed', 'account_name'], name='unique_feed_account')
        ]
    def __str__(self):
        return f"{self.feed.feed_name} - {self.account_name}"
    
class Article(models.Model):
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    site_name = models.CharField(max_length=255)
    posted_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'article'],name='unique_favorite')
        ]