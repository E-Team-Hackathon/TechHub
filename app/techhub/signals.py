from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.management import call_command
from techhub.models import Contributor

@receiver(post_save, sender=Contributor)
def fetch_articles_after_contributor_save(sender, instance, created, **kwargs):
  # 投稿者が登録されたらfetch＿articlesが発動される

  if created :
    call_command("fetch_articles")