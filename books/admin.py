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

class BookAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["title", "authors", "publisher"]}),
        ("Date information", {
            "fields": ["publication_date"],
            "classes": ["collapse"], # make this section collapsible, 
        }),
    ]
    list_display = ["title", "publisher", "author", "was_published_recently"]
    list_filter = ["publication_date"] #on the table's right side
    search_fields = ["title"]
    filter_horizontal = ["authors"]  # for ManyToManyField

class BookInline(admin.StackedInline): # Inline for books in publisher admin
    #TabularInline can also be used for a more compact layout
    model = Book
    extra = 3

class PublisherAdmin(admin.ModelAdmin):
    inlines = [BookInline] #inheriting BookInline

admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Publisher, PublisherAdmin)