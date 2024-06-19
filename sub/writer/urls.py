from django.urls import path
from .views import (writer_profile_view, create_article, read_articles, editing_articles, delete_articles, update_profiles, delete_writer)

urlpatterns = [
    path('writer-profile/', writer_profile_view.as_view(), name='writer-profile'),
    path('add-article/', create_article.as_view(),name='writer-add-article'),
    path('your-articles/', read_articles.as_view(),name='read-articles'),
    path('edit-article/<int:pk>/', editing_articles.as_view(),name='edit-articles'),
    path('delete-article/<int:pk>/', delete_articles.as_view(),name='delete-articles'),
    path('edit-profile/', update_profiles.as_view(),name='update-profile'),
    path('delete-account/', delete_writer.as_view(),name='delete-account'),
]
