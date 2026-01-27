from django import forms
from .models import Book, Author, Publisher, Classification

class AuthorSearchForm(forms.Form):
    query = forms.CharField(required=False, label="Search Author")

class PublisherSearchForm(forms.Form):
    query = forms.CharField(required=False, label="Search Publisher")

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
        error_messages = {
            'title': {'required': "Book title is required!"},
            'publication_date': {'invalid': "Enter a valid date in YYYY-MM-DD format."},
        }

class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = "__all__"
        error_messages = {
            'name': {'required': "Publisher name is required!"},
            'address': {'invalid': "Enter a valid address."},
        }