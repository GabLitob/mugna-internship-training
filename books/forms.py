from django import forms
from .models import Book, Author, Publisher, Classification
from django.contrib.auth.models import User # For user registration. why? To create new users in the system.
from django.contrib.auth.forms import UserCreationForm  

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

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = "__all__"
        error_messages = {
            'first_name': {'required': "Author's first name is required!"},
            'last_name': {'required': "Author's last name is required!"},
            'email': {'invalid': "Enter a valid email address."},
        }


# Users and Authentication form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password") #PasswordInput to hide input


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ["username", "password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match!")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user