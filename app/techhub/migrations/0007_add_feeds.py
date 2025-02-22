from django.db import migrations

def add_default_feeds(apps, schema_editor):
    Feed = apps.get_model('techhub', 'Feed')

    feeds = [
        {'feed_name': 'Qiita', 'feed_url': 'http://qiita.com/{account_name}/feed.atom'},
        {'feed_name': 'Zenn','feed_url': 'https://zenn.dev/{account_name}/feed'},
    ]

    for feed in feeds:
        Feed.objects.get_or_create(feed_name=feed['feed_name'], defaults={'feed_url': feed['feed_url']})

class Migration(migrations.Migration):

    dependencies = [
        ('techhub', "0006_favorite_unique_favorite"), 
    ]

    operations = [
        migrations.RunPython(add_default_feeds),
    ]
