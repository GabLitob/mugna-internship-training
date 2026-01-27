from django.shortcuts import redirect, render, get_object_or_404
from .models import Book, Author, Classification, Publisher
from .forms import (AuthorSearchForm, PublisherSearchForm, BookForm, PublisherForm,)


# 1. List all books
def book_list(request):
    books = Book.objects.all()  # Get all books from database
    return render(request, 'books/book_list.html', {'books': books})


# 2. Show details of a single book
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)  # Get book or show 404 error
    return render(request, 'books/book_detail.html', {'book': book})

# 3.List all authors with search functionality
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
def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)  # Get author
    books = author.books.all()  # Get all books by this author (using related_name)
    return render(request, 'books/author_detail.html', {'author': author, 'books': books})


# 5. List all publishers with search functionality
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
def classification_list(request):
    classifications = Classification.objects.all()  # Get all classifications
    return render(request, 'books/classification_list.html', {'classifications': classifications})


# 7. Show all books in a classification
def classification_detail(request, classification_id):
    classification = get_object_or_404(Classification, id=classification_id)  # Get classification
    books = classification.books.all()  # Get all books in this classification
    return render(request, 'books/classification_detail.html', {'classification': classification, 'books': books})



#Book CRUD

def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm()

    return render(request, "books/book_form.html", {"form": form})

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

def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        book.delete()
        return redirect("book_list")

    return render(request, "books/book_confirm_delete.html", {"book": book})


#Publisher CRUD

def publisher_create(request):
    if request.method == "POST":
        form = PublisherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("publisher_list")
    else:
        form = PublisherForm()

    return render(request, "books/publisher_form.html", {"form": form})

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

def publisher_delete(request, publisher_id):
    publisher = get_object_or_404(Publisher, id=publisher_id)

    if request.method == "POST":
        publisher.delete()
        return redirect("publisher_list")

    return render(request, "books/publisher_confirm_delete.html", {"publisher": publisher})