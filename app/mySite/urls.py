from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from accounts.views import profile, SignUpView, CustomLoginView, mypage
from techhub.views import toggle_favorite, article_search, contributor_filtering

# MEDIA_URL のリクエストを MEDIA_ROOT にマッピングする
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', SignUpView.as_view(template_name='signup.html'), name='signup'),
    path('login/',CustomLoginView.as_view(redirect_authenticated_user=True,template_name='login.html'),name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('profile/', login_required(profile), name='profile'),
    path('mypage/', login_required(mypage), name='mypage'),
    path('techhub/', include('techhub.urls')),
    path('search/', article_search, name='search'),
    path('favorite/<int:article_id>', login_required(toggle_favorite), name='toggle_favorite'),
    path('contributor_filtering/', contributor_filtering, name='contributor_filtering'),
    path('filtering/<str:username>/', contributor_filtering, name='contributor_filtering_by_username'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # MEDIA