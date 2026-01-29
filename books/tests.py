import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse  # FIXED: Added missing import
from django.contrib.auth.models import User  # FIXED: Added for authentication tests

from .models import Book, Author, Publisher, Classification  # FIXED: Added missing models



class BookMethodTests(TestCase):
#    def test_was_published_recently_with_future_book(self): # these are test clients
#        """
#        was_published_recently() should return False for books
#        whose publication_date is in the future.
#        """
#        future_date = timezone.now().date() + datetime.timedelta(days=30)
#        future_book = Book(publication_date=future_date)
#        self.assertFalse(future_book.was_published_recently())

    def test_was_published_recently_with_old_book(self): # these are test clients
        """
        was_published_recently() should return False for books whose
        publication_date is older than 1 day.
        """

        pub_date = timezone.now().date() - datetime.timedelta(days=30)
        old_book = Book(publication_date=pub_date)
        self.assertFalse(old_book.was_published_recently())

class IndexViewTests(TestCase):
    def setUp(self):
        # FIXED: Added classification (required by Book model)
        self.classification = Classification.objects.create(
            code="FIC",
            name="Fiction",
            description="Fiction books"
        )
        self.publisher = Publisher.objects.create(
            name="test",
            address="test",
            city="test",
            state_province="test",
            country="test",
            website="http://test.com",  # FIXED: Valid URL format
        )
        self.author = Author.objects.create(
            first_name="test",
            last_name="test",
            email="test@gmail.com"
        )
        self.book = Book.objects.create(
            title="test",
            publisher=self.publisher,
            classification=self.classification,  # FIXED: Added classification
            publication_date=timezone.now().date()  # FIXED: Use .date()
        )
        self.book.authors.add(self.author)

    #test ordering is important such as these two:
    #test_index_view_with_books should be before test_index_view_with_no_books
    #since the latter deletes all books.
    #if with_no_books is before with_books, it will delete the test db and 
    # the with_books test will fail.
    #In CRUD, delete should comes last, so that other tests methods 
    # can use the data created in setUp
    #This is a rule of thumb to follow in testing
    def test_index_view_with_books(self):
        """Books should be displayed if some books exist."""
        response = self.client.get(reverse("index")) #reverse() usage in general is? 
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(list(response.context["books"]),list(Book.objects.all()))

    def test_index_view_with_no_books(self):
        """Display appropriate message if no books exist."""
        Book.objects.all().delete()
        response = self.client.get(reverse("index"))
        self.assertContains(response, "No books are available.")
        self.assertListEqual(list(response.context["books"]),[])


# ========== NEW TESTS FOR THE EXERCISE ==========

class LoginViewTests(TestCase):
    """Tests for login functionality"""
    
    def setUp(self):
        """Create a test user"""
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
    
    def test_login_view_loads(self):
        """Login page should load successfully"""
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "login")  # Check if login form is present
    
    def test_login_with_valid_credentials(self):
        """User should be able to login with correct credentials"""
        response = self.client.post(reverse("login"), {
            "username": "testuser",
            "password": "testpass123"
        })
        # After successful login, should redirect to book_list
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("book_list"))
    
    def test_login_with_invalid_credentials(self):
        """User should not be able to login with wrong password"""
        response = self.client.post(reverse("login"), {
            "username": "testuser",
            "password": "wrongpassword"
        })
        # Should stay on login page with error
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password")


class LogoutViewTests(TestCase):
    """Tests for logout functionality"""
    
    def setUp(self):
        """Create and login a test user"""
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")
    
    def test_logout_redirects_to_login(self):
        """After logout, user should be redirected to login page"""
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))
    
    def test_user_is_logged_out(self):
        """User should no longer be authenticated after logout"""
        self.client.get(reverse("logout"))
        # Try to access protected page - should redirect to login
        response = self.client.get(reverse("book_list"))
        self.assertEqual(response.status_code, 302)


class DetailViewTests(TestCase):
    """Tests for detail view (the detail function from views.py)"""
    
    def setUp(self):
        """Create test data"""
        self.classification = Classification.objects.create(
            code="FIC",
            name="Fiction",
            description="Fiction books"
        )
        self.publisher = Publisher.objects.create(
            name="Test Publisher",
            address="123 Test St",
            city="Test City",
            state_province="Test State",
            country="Test Country",
            website="http://test.com",
        )
        self.author = Author.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@test.com"
        )
        self.book = Book.objects.create(
            title="Test Book",
            publisher=self.publisher,
            classification=self.classification,
            publication_date=timezone.now().date()
        )
        self.book.authors.add(self.author)
    
    def test_detail_view_with_valid_book(self):
        """Detail view should display book information"""
        response = self.client.get(reverse("detail", args=[self.book.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["book"], self.book)
        self.assertContains(response, "Test Book")
    
    def test_detail_view_with_invalid_book(self):
        """Detail view should return 404 for non-existent book"""
        response = self.client.get(reverse("detail", args=[9999]))
        self.assertEqual(response.status_code, 404)


class AuthorSearchViewTests(TestCase):
    """Tests for author list with search functionality"""
    
    def setUp(self):
        """Create test authors and login"""
        # Create user and login (author_list requires login)
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")
        
        # Create test authors
        self.author1 = Author.objects.create(
            first_name="John",
            last_name="Smith",
            email="john@test.com"
        )
        self.author2 = Author.objects.create(
            first_name="Jane",
            last_name="Doe",
            email="jane@test.com"
        )
        self.author3 = Author.objects.create(
            first_name="Bob",
            last_name="Johnson",
            email="bob@test.com"
        )
    
    def test_author_list_displays_all_authors(self):
        """Author list should show all authors when no search query"""
        response = self.client.get(reverse("author_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["authors"]), 3)
    
    def test_author_search_by_first_name(self):
        """Search should find authors by first name"""
        response = self.client.get(reverse("author_list"), {"query": "John"})
        self.assertEqual(response.status_code, 200)
        authors = list(response.context["authors"])
        self.assertIn(self.author1, authors)  # John Smith
        self.assertIn(self.author3, authors)  # Bob Johnson (contains 'John')
    
    def test_author_search_by_last_name(self):
        """Search should find authors by last name"""
        response = self.client.get(reverse("author_list"), {"query": "Doe"})
        self.assertEqual(response.status_code, 200)
        authors = list(response.context["authors"])
        self.assertIn(self.author2, authors)
        self.assertEqual(len(authors), 1)


class AuthorCreateViewTests(TestCase):
    """Tests for adding new authors"""
    
    def setUp(self):
        """Create admin user and login"""
        self.admin_user = User.objects.create_user(
            username="admin",
            password="adminpass123",
            is_staff=True  # Admin user can create authors
        )
        self.client.login(username="admin", password="adminpass123")
    
    def test_author_create_view_loads(self):
        """Author create form should load for admin users"""
        response = self.client.get(reverse("author_create"))
        self.assertEqual(response.status_code, 200)
    
    def test_author_create_with_valid_data(self):
        """New author should be created with valid data"""
        initial_count = Author.objects.count()
        response = self.client.post(reverse("author_create"), {
            "first_name": "New",
            "last_name": "Author",
            "email": "new@test.com"
        })
        # Should redirect after successful creation
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Author.objects.count(), initial_count + 1)
        # Verify the author was created
        new_author = Author.objects.get(email="new@test.com")
        self.assertEqual(new_author.first_name, "New")
        self.assertEqual(new_author.last_name, "Author")
    
    def test_author_create_requires_admin(self):
        """Non-admin users should not be able to create authors"""
        # Logout and login as regular user
        self.client.logout()
        regular_user = User.objects.create_user(
            username="regular",
            password="pass123",
            is_staff=False
        )
        self.client.login(username="regular", password="pass123")
        
        response = self.client.get(reverse("author_create"))
        # Should redirect (not allowed)
        self.assertEqual(response.status_code, 302)


class AuthorDeleteTests(TestCase):
    """Tests for deleting authors (demonstrating delete operation)"""
    
    def setUp(self):
        """Create test author"""
        self.author = Author.objects.create(
            first_name="Delete",
            last_name="Me",
            email="delete@test.com"
        )
    
    def test_author_can_be_deleted(self):
        """Author should be deleted successfully"""
        initial_count = Author.objects.count()
        author_id = self.author.id
        
        # Verify author exists
        self.assertTrue(Author.objects.filter(pk=author_id).exists())
        
        # Delete the author
        self.author.delete()
        
        # Verify deletion
        self.assertEqual(Author.objects.count(), initial_count - 1)
        self.assertFalse(Author.objects.filter(pk=author_id).exists())