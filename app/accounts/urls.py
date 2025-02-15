from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
# MEDIA_URL のリクエストを MEDIA_ROOT にマッピングする
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path(
        'login/',
        auth_views.LoginView.as_view(redirect_authenticated_user=True,template_name='accounts/login.html'),
        name='login'
    ),
    path('profile/', views.profile, name='profile'),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # MEDIA