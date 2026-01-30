from django.core.management.base import BaseCommand, CommandError
from books.models import Author

class Command(BaseCommand):
    help = 'Removes the author from the given ids'


    def add_arguments(self, parser): 
        # It defines the command-line arguments that the management command accepts.
        # Positional argument
        parser.add_argument('author_ids', nargs='+', type=int)

        # Optional argument
        # parser.add_argument(
        #     "--delete",
        #     action="store_true",
        #     help="Delete author instead of deactivating",
        # )

    def handle(self, *args, **options): 
        # processes the command-line arguments and performs the action of 
        # removing authors based on the provided IDs.
        for author_id in options['author_ids']:
            try:
                author = Author.objects.get(id=author_id)
                author.delete()
                self.stdout.write(self.style.SUCCESS(f'Successfully removed author with id {author_id}'))
            except Author.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Author with id {author_id} does not exist'))
            '''
            if options["delete"]:
                author.delete()
                # for optional argument --delete
            '''
            author.active = False
            author.save()

            self.stdout.write(self.style.SUCCESS(f'Successfully removed author with id {author_id}'))   


