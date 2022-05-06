from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include

from . import views as mysite_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(next_page='/'),
         name='logout'),
    path("accounts/signup/", mysite_views.SignUp.as_view(), name="signup"),
    path('user_edit/', mysite_views.user_edit, name='user_edit'),
    path('', include('blog.urls'))
]
