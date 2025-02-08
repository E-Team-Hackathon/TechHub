import feedparser
from urllib.parse import urlparse
from django.core.management.base import BaseCommand
from techhub.models import Feed, Contributor, Article
from datetime import datetime

class Command(BaseCommand):
    help = "RSSフィードから記事を取得して保存"

    def handle(self, *args, **kwargs):
        feeds = Feed.objects.all()  # Feed テーブルのすべてのフィードを取得

        for feed in feeds:
            contributors = Contributor.objects.filter(feed=feed) #記事サイトを絞って投稿者情報を取得
            if not contributors.exists():
                #self.stdoutデバッグ用
                self.stdout.write(self.style.WARNING(f"No contributors found for {feed.feed_name}, skipping articles."))
                continue  # Contributor がいない場合はスキップ

            for contributor in contributors:
                # `feed_url` の `{account_name}` を `contributor.account_name` に置換
                feed_url = feed.feed_url.format(account_name=contributor.account_name)

                domain = urlparse(feed_url).netloc.split(".")[0]  # ドメイン名を取得
                feed_data = feedparser.parse(feed_url)

                self.stdout.write(f"Fetching articles from {domain} ({feed_url})...")

                if not feed_data.entries:
                    self.stdout.write(self.style.WARNING(f"No articles found for {domain} ({feed_url})"))
                    continue

                for entry in feed_data.entries:
                    if Article.objects.filter(url=entry.link).exists():
                        continue  # 既に存在する記事はスキップ

                    # Qiita: published, Zenn: pubDate
                    posted_at = entry.get("published") or entry.get("pubDate")
                    try:
                        posted_at = datetime.strptime(posted_at, "%Y-%m-%dT%H:%M:%S%z") if posted_at else datetime.utcnow()
                    except ValueError:
                        posted_at = datetime.utcnow()

                    # 記事を保存
                    Article.objects.create(
                        contributor=contributor,
                        title=entry.title,
                        url=entry.link,
                        site_name=domain,
                        posted_at=posted_at
                    )

                    print(f'#100: Contributor -> {contributor.account_name}')
                    self.stdout.write(self.style.SUCCESS(f"Saved: {entry.title} ({domain})"))
