from django.urls import path
from .views import *

urlpatterns = [
    path('', ArticleListView.as_view(), name='index'),
    path('category/<int:pk>', ArticleListByCategory.as_view(), name='category'),
    path('article/<int:pk>', article_view, name='article'),
    path('add_article/', NewArticle.as_view(), name='add_article'),
    path('article/<int:pk>/update/', ArticleUpdate.as_view(), name='update'),
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='delete'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('search/', SearchResults.as_view(), name='search'),
    path('register/', register, name='register'),
    path('save_comment/<int:pk>/', save_comment, name='save_comment'),
    path('profile/<int:pk>/', profile_view, name='profile'),
    path('delete_comment/<int:pk>', delete_comment, name='delete_comment'),
    path('edit_comment/<int:article_id>/<int:comment_id>', edit_comment, name='edit_comment'),
    path('save_edited_comment/<int:pk>', save_edited_comment, name='save_edited_comment'),
    path('about_site/', about_site, name='about_site'),
]
