from django.contrib import admin
from .models import Feed, Article, Contributor

admin.site.register(Feed)
admin.site.register(Article)
admin.site.register(Contributor)