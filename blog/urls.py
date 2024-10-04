from django.urls import path
from .views import post_create_view, post_delete_view, post_detail_view, post_list_view, post_update_view,category_user_view, tag_user_view

urlpatterns = [
    path('', post_list_view, name='post_list'),
    path('post/<int:pk>/', post_detail_view, name='post_detail'),
    path('post/new/', post_create_view, name='post_create'),
    path('post/<int:pk>/edit/', post_update_view, name='post_update'),
    path('post/<int:pk>/delete/', post_delete_view, name='post_delete'),
    path('category/new', category_user_view, name='category_add'),
    path('tag/new', tag_user_view, name='tag_add')
]