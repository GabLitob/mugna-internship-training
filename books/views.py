from django.shortcuts import render, get_object_or_404
from .models import Book, Author, Classification


# 1. List all books
def book_list(request):
    books = Book.objects.all()  # Get all books from database
    return render(request, 'books/book_list.html', {'books': books})


# 2. Show details of a single book
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)  # Get book or show 404 error
    return render(request, 'books/book_detail.html', {'book': book})


# 3. Show author details and their books
def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)  # Get author
    books = author.books.all()  # Get all books by this author (using related_name)
    return render(request, 'books/author_detail.html', {'author': author, 'books': books})


# 4. List all classifications
def classification_list(request):
    classifications = Classification.objects.all()  # Get all classifications
    return render(request, 'books/classification_list.html', {'classifications': classifications})


# 5. Show all books in a classification
def classification_detail(request, classification_id):
    classification = get_object_or_404(Classification, id=classification_id)  # Get classification
    books = classification.books.all()  # Get all books in this classification
    return render(request, 'books/classification_detail.html', {'classification': classification, 'books': books})
