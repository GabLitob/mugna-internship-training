# books/urls.py
from django.urls import path
from . import views

urlpatterns = [
    #Authentication 
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),

    # App
    path('', views.book_list, name='book_list'),  # /books/
    path('add/', views.book_create, name='book_create'),  # /books/add/
    path('<int:book_id>/', views.book_detail, name='book_detail'),
    path('<int:book_id>/edit/', views.book_update, name='book_update'),
    path('<int:book_id>/delete/', views.book_delete, name='book_delete'),
    path('authors/<int:author_id>/', views.author_detail, name='author_detail'),
    path('classifications/', views.classification_list, name='classification_list'),
    path('classifications/<int:classification_id>/', views.classification_detail, name='classification_detail'),
    path('authors/', views.author_list, name='author_list'),
    path('authors/add/', views.author_create, name='author_create'),
    path('publishers/', views.publisher_list, name='publisher_list'),
    path('publishers/add/', views.publisher_create, name='publisher_create'),
    path('publishers/<int:publisher_id>/edit/', views.publisher_update, name='publisher_update'),
    path('publishers/<int:publisher_id>/delete/', views.publisher_delete, name='publisher_delete'),
]
