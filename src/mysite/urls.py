from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include

from . import views as blog_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(next_page='/'),
         name='logout'),
    path("accounts/signup/", blog_views.SignUp.as_view(), name="signup"),
    path('', include('blog.urls'))
]
