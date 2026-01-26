from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),  # List all books at /books/
    path('<int:book_id>/', views.book_detail, name='book_detail'),  # /books/1/
    path('authors/<int:author_id>/', views.author_detail, name='author_detail'),  # /books/authors/1/
    path('classifications/', views.classification_list, name='classification_list'),  # /books/classifications/
    path('classifications/<int:classification_id>/', views.classification_detail, name='classification_detail'),  # /books/classifications/1/
]
