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
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


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
class AuthorListView(LoginRequiredMixin, ListView):
    model = Author
    template_name = 'books/author_list.html'
    context_object_name = 'authors'

    def get_queryset(self):
        queryset = Author.objects.all()
        form = AuthorSearchForm(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data.get("query")
            if query:
                words = query.split()
                for word in words:
                    queryset = queryset.filter(
                        first_name__icontains=word
                    ) | queryset.filter(last_name__icontains=word)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AuthorSearchForm(self.request.GET)
        return context


# 4. Show author details and their books
@login_required
def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)  # Get author
    books = author.books.all()  # Get all books by this author (using related_name)
    return render(request, 'books/author_detail.html', {'author': author, 'books': books})


# 5. List all publishers with search functionality
class PublisherListView(LoginRequiredMixin, ListView):
    model = Publisher
    template_name = 'books/publisher_list.html'
    context_object_name = 'publishers'

    def get_queryset(self):
        queryset = Publisher.objects.all()
        form = PublisherSearchForm(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data.get("query")
            if query:
                words = query.split()
                for word in words:
                    queryset = queryset.filter(name__icontains=word)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PublisherSearchForm(self.request.GET)
        return context



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
class BookCreateView(UserPassesTestMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('book_list')

    def test_func(self):
        return is_admin(self.request.user)

class BookUpdateView(UserPassesTestMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    pk_url_kwarg = 'book_id'

    def test_func(self):
        return is_admin(self.request.user)

    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'book_id': self.object.pk})

class BookDeleteView(UserPassesTestMixin, DeleteView):
    model = Book
    template_name = 'books/book_confirm_delete.html'
    success_url = reverse_lazy('book_list')
    pk_url_kwarg = 'book_id'
    context_object_name = 'book'

    def test_func(self):
        return is_admin(self.request.user)


#Publisher CRUD
class PublisherCreateView(UserPassesTestMixin, CreateView):
    model = Publisher
    form_class = PublisherForm
    template_name = 'books/publisher_form.html'
    success_url = reverse_lazy('publisher_list')

    def test_func(self):
        return is_admin(self.request.user)

class PublisherUpdateView(UserPassesTestMixin, UpdateView):
    model = Publisher
    form_class = PublisherForm
    template_name = 'books/publisher_form.html'
    success_url = reverse_lazy('publisher_list')
    pk_url_kwarg = 'publisher_id'

    def test_func(self):
        return is_admin(self.request.user)

class PublisherDeleteView(UserPassesTestMixin, DeleteView):
    model = Publisher
    template_name = 'books/publisher_confirm_delete.html'
    success_url = reverse_lazy('publisher_list')
    pk_url_kwarg = 'publisher_id'
    context_object_name = 'publisher'

    def test_func(self):
        return is_admin(self.request.user)


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


#unit tests views for index and detail
def index(request):
    books = Book.objects.all()
    return render(request, "books/books.html", {"books": books})


def detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        raise Http404()

    return render(request, "books/book.html", {"book": book})