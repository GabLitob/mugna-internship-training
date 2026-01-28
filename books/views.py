from django.shortcuts import redirect, render, get_object_or_404
from .models import Book, Author, Classification, Publisher
from .forms import (
    AuthorSearchForm, 
    PublisherSearchForm, 
    BookForm, 
    PublisherForm, 
    AuthorForm,
    LoginForm, 
    RegisterForm
    )
from django.contrib.auth import authenticate, login, logout # For user authentication
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required, user_passes_test # To restrict access to authenticated users only



#Users and Authentication views

def is_admin(user):
    return user.is_staff # Check if user is admin/staff

def login_view(request):
    form = LoginForm(request.POST or None)
    error = None

    if request.method == "POST" and form.is_valid():
        user = authenticate(
            username=form.cleaned_data["username"], # what is cleaned_data? cleaned_data is a dictionary containing validated form input data
            password=form.cleaned_data["password"]
        )
        if user:
            login(request, user)
            return redirect("book_list")
        else:
            error = "Invalid username or password"

    return render(request, "books/login.html", {
        "form": form,
        "error": error
    })


def register_view(request):
    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("login")

    return render(request, "books/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")   


# 1. List all books
@login_required # will this be rendered to book_list? Yes, it will restrict access to the book_list view to authenticated users only.
def book_list(request):
    books = Book.objects.all()  # Get all books from database
    return render(request, 'books/book_list.html', {'books': books})


# 2. Show details of a single book
@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)  # Get book or show 404 error
    return render(request, 'books/book_detail.html', {'book': book})

# 3.List all authors with search functionality
@login_required
def author_list(request):
    form = AuthorSearchForm(request.GET)
    authors = Author.objects.all()

    if form.is_valid():
        query = form.cleaned_data["query"]
        if query:
            words = query.split()  # split by spaces
            for word in words:
                authors = authors.filter(
                    first_name__icontains=word
                ) | authors.filter(last_name__icontains=word)

    return render(request, "books/author_list.html", {
        "form": form,
        "authors": authors.distinct()  # avoid duplicates
    })


# 4. Show author details and their books
@login_required
def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)  # Get author
    books = author.books.all()  # Get all books by this author (using related_name)
    return render(request, 'books/author_detail.html', {'author': author, 'books': books})


# 5. List all publishers with search functionality
@login_required
def publisher_list(request):
    form = PublisherSearchForm(request.GET)
    publishers = Publisher.objects.all()

    if form.is_valid():
        query = form.cleaned_data["query"]
        if query:
            words = query.split()
            for word in words:
                publishers = publishers.filter(name__icontains=word)

    return render(request, "books/publisher_list.html", {
        "form": form,
        "publishers": publishers.distinct()
    })



# 6. List all classifications
@login_required 
def classification_list(request):
    classifications = Classification.objects.all()  # Get all classifications
    return render(request, 'books/classification_list.html', {'classifications': classifications})


# 7. Show all books in a classification
@login_required
def classification_detail(request, classification_id):
    classification = get_object_or_404(Classification, id=classification_id)  # Get classification
    books = classification.books.all()  # Get all books in this classification
    return render(request, 'books/classification_detail.html', {'classification': classification, 'books': books})



#Book CRUD
@user_passes_test(is_admin)  # Only admin users can create books
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm()

    return render(request, "books/book_form.html", {"form": form})

@user_passes_test(is_admin)
def book_update(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_detail", book_id=book.id)
    else:
        form = BookForm(instance=book)

    return render(request, "books/book_form.html", {"form": form})

@user_passes_test(is_admin)
def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        book.delete()
        return redirect("book_list")

    return render(request, "books/book_confirm_delete.html", {"book": book})


#Publisher CRUD
@user_passes_test(is_admin) # Only admin users can create publishers
def publisher_create(request):
    if request.method == "POST":
        form = PublisherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("publisher_list")
    else:
        form = PublisherForm()

    return render(request, "books/publisher_form.html", {"form": form})

@user_passes_test(is_admin)
def publisher_update(request, publisher_id):
    publisher = get_object_or_404(Publisher, id=publisher_id)

    if request.method == "POST":
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            form.save()
            return redirect("publisher_list")
    else:
        form = PublisherForm(instance=publisher)

    return render(request, "books/publisher_form.html", {"form": form})

@user_passes_test(is_admin)
def publisher_delete(request, publisher_id):
    publisher = get_object_or_404(Publisher, id=publisher_id)

    if request.method == "POST":
        publisher.delete()
        return redirect("publisher_list")

    return render(request, "books/publisher_confirm_delete.html", {"publisher": publisher})


#Author CRUD
@user_passes_test(is_admin)  # Only admin users can create authors
def author_create(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("author_list")
    else:
        form = AuthorForm()

    return render(request, "books/author_form.html", {"form": form})


