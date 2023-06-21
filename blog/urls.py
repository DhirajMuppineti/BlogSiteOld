from django.contrib import admin
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.BaseView.as_view(), name='all'),
    path('main', views.MainView.as_view(), name='main'),
    path('main/like/<int:pk>/', views.like_blog, name='like_post'),
    path('main/create/', views.BlogCreate.as_view(), name='write_blog'),
    path('main/<int:pk>/update/', views.BlogUpdate.as_view(), name='update_blog'),
    path('main/<int:pk>/delete/', views.BlogDelete.as_view(), name='delete_blog'),
    path('main/<int:pk>/',views.BlogRead.as_view(),name='read_blog'),
    path('main/<int:pk>/comment/',views.CommentBlog.as_view(),name='comment_blog'),
    path('register',views.register_request,name='signup'),
]