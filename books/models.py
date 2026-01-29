from django.db import models
import datetime
from django.utils import timezone


class Classification(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.code} - {self.name}"


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state_province = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    website = models.URLField()

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField("e-mail")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author, related_name="books")
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        related_name="books"
    )
    classification = models.ForeignKey(
        Classification,
        on_delete=models.PROTECT,
        related_name="books"
    )
    publication_date = models.DateField()

    def __str__(self):
        return self.title

    def author(self):
        """Used by Django admin list_display"""
        return ", ".join(str(a) for a in self.authors.all())

    author.short_description = "Author(s)"

    def was_published_recently(self):
        """Returns True if the book was published within the last day, False otherwise."""
        today = timezone.now().date()
        # Check if publication date is not in the future and within the last day
        return today - datetime.timedelta(days=1) <= self.publication_date <= today

    '''
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    publication_date = models.DateField()

    def was_published_recently(self):
        """
        Returns True if the book was published 1 day ago. False if not.
        """
        date_today = timezone.now().date()
        return date_today - datetime.timedelta(days=1) <= self.publication_date <= date_today


    def __str__(self):
        return self.title
    
    '''
