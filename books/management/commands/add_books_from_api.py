import requests
from django.core.management.base import BaseCommand, CommandError
from books.models import Author, Book, Publisher, Classification
from datetime import datetime


class Command(BaseCommand):
    help = 'Fetches books and authors from Gutendex API and adds them to the database'

    def add_arguments(self, parser):
        # POSITIONAL: search term
        parser.add_argument(
            'search_term',
            nargs='?',
            type=str,
            default='',
            help='Search term to filter books'
        )
        
        # OPTIONAL: --limit flag
        parser.add_argument(
            '--limit',
            type=int,
            default=10,
            help='Number of books to import (default: 10)'
        )

    def handle(self, *args, **options): # what does this method do in this context? 
        limit = options['limit'] 
        search_term = options['search_term']
        
        try:
            # Build API URL
            url = 'https://gutendex.com/books/'
            if search_term:
                url += f'?search={search_term}'
                self.stdout.write(f'Fetching books matching "{search_term}"...')
            else:
                self.stdout.write('Fetching books from Gutendex API...')
            
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            books_data = data.get('results', [])[:limit]
            
            if not books_data:
                self.stdout.write(self.style.WARNING('No books found'))
                return
            
            # Get or create default publisher and classification
            publisher, _ = Publisher.objects.get_or_create(
                name='Project Gutenberg',
                defaults={
                    'address': 'Unknown',
                    'city': 'Unknown',
                    'state_province': 'Unknown',
                    'country': 'USA',
                    'website': 'https://www.gutenberg.org'
                }
            )
            
            classification, _ = Classification.objects.get_or_create(
                code='GUT',
                defaults={
                    'name': 'Gutenberg Collection',
                    'description': 'Books from Project Gutenberg'
                }
            )
            
            books_created = 0
            authors_created = 0
            
            # Process each book
            for book_data in books_data:
                title = book_data.get('title', 'Unknown Title')
                
                # Skip if book exists
                if Book.objects.filter(title=title).exists():
                    self.stdout.write(self.style.WARNING(f'"{title}" already exists, skipping...'))
                    continue
                
                # Create book
                book = Book.objects.create(
                    title=title[:100],
                    publisher=publisher,
                    classification=classification,
                    publication_date=datetime.now().date()
                )
                books_created += 1
                
                # Process authors
                for author_data in book_data.get('authors', []):
                    name = author_data.get('name', 'Unknown')
                    
                    # Parse name: "Last, First" or "First Last"
                    if ', ' in name:
                        last_name, first_name = name.split(', ', 1)
                    else:
                        parts = name.split(' ', 1)
                        first_name = parts[0]
                        last_name = parts[1] if len(parts) > 1 else ''
                    
                    # Get or create author
                    author, created = Author.objects.get_or_create(
                        first_name=first_name[:30],
                        last_name=last_name[:40],
                        defaults={'email': f'{first_name.lower()}@gutenberg.org'[:254]}
                    )
                    
                    if created:
                        authors_created += 1
                    
                    book.authors.add(author)
                
                self.stdout.write(self.style.SUCCESS(f'✓ "{title}"'))
            
            # Summary
            self.stdout.write(self.style.SUCCESS(
                f'\n=== Complete ==='
                f'\nBooks: {books_created}'
                f'\nAuthors: {authors_created}'
            ))
            
        except requests.RequestException as e:
            raise CommandError(f'API error: {e}')
        except Exception as e:
            raise CommandError(f'Error: {e}')
