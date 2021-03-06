from django.urls import path
from . import views


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('subscriptions_list/', views.subscriptions_list,
         name='subscriptions_list'),
    path('user/<str:username>/', views.user_detail, name='user_detail'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:pk>/add_like/', views.add_like, name='add_like'),
    path('post/<int:pk>/add_dislike/', views.add_dislike, name='add_dislike'),
    path('post/<int:pk>/subscribe/', views.subscribe, name='subscribe'),
]
