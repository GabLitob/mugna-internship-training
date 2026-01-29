# books/urls.py
from django.urls import path
from . import views

urlpatterns = [
    #Authentication 
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),

    # App
    path('', views.book_list, name='book_list'),
    path('index/', views.index, name='index'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('add/', views.BookCreateView.as_view(), name='book_create'),
    path('<int:book_id>/', views.book_detail, name='book_detail'),
    path('<int:book_id>/edit/', views.BookUpdateView.as_view(), name='book_update'),
    path('<int:book_id>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
    path('authors/<int:author_id>/', views.author_detail, name='author_detail'),
    path('classifications/', views.classification_list, name='classification_list'),
    path('classifications/<int:classification_id>/', views.classification_detail, name='classification_detail'),
    path('authors/', views.AuthorListView.as_view(), name='author_list'),
    path('authors/add/', views.author_create, name='author_create'),
    path('publishers/', views.PublisherListView.as_view(), name='publisher_list'),
    path('publishers/add/', views.PublisherCreateView.as_view(), name='publisher_create'),
    path('publishers/<int:publisher_id>/edit/', views.PublisherUpdateView.as_view(), name='publisher_update'),
    path('publishers/<int:publisher_id>/delete/', views.PublisherDeleteView.as_view(), name='publisher_delete'),
]
