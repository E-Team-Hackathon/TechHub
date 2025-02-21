from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts.views import profile, SignUpView, mypage
# MEDIA_URL のリクエストを MEDIA_ROOT にマッピングする
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', SignUpView.as_view(template_name='signup.html'), name='signup'),
    path(
        'login/',
        auth_views.LoginView.as_view(redirect_authenticated_user=True,template_name='login.html'),
        name='login'
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('profile/', profile, name='profile'),
    path('mypage/', mypage, name='mypage'),
    path('techhub/', include('techhub.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # MEDIA