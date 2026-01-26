from django.contrib import admin

from .models import Author, Book, Publisher


class AuthorAdmin(admin.ModelAdmin):
    fields = ["email", "first_name", "last_name"]

class BookAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["title", "authors", "publisher"]}),
        ("Date information", {
            "fields": ["publication_date"],
        }),
    ]

admin.site.register(Author, AuthorAdmin)
admin.site.register(Book)
admin.site.register(Publisher)