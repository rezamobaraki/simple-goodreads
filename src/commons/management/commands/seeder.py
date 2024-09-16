from django.core.management import BaseCommand

from accounts.factories.user import UserFactory
from books.factories.book import BookFactory
from books.factories.bookmark import BookmarkFactory
from books.factories.review import ReviewFactory


class Command(BaseCommand):
    help = 'Seeder is a command to seed the database'

    def add_arguments(self, parser):
        parser.add_argument('-u', '--user', type=int, help='Number of User to create')
        parser.add_argument('-b', '--book', type=int, help='Number of Book to create')
        parser.add_argument('-r', '--review', type=int, help='Number of Review to create')
        parser.add_argument('-m', '--bookmark', type=int, help='Number of Bookmark to create')

    def handle(self, *args, **options):
        self.stdout.write('Starting to seed the database...')
        user_count = options['user']
        book_count = options['book']
        review_count = options['review']
        bookmark_count = options['bookmark']

        user_instances = []
        user_data_output = []
        book_instances = []
        review_instances = []
        bookmark_instances = []

        admin_user = UserFactory()
        admin_user.is_superuser = True
        admin_user.is_staff = True
        admin_user.save()
        user_data_output.append(
            f'\nAdmin User Details:\n'
            f'  Email: {admin_user.email}\n'
            f'  Password: new_password\n'
        )

        if user_count:
            for i in range(user_count):
                user = UserFactory()
                user_data_output.append(
                    f'\nUser-{user.id} Details:\n'
                    f'  Email: {user.email}\n'
                    f'  Password: new_password\n'
                )
                user_instances.append(user)
                self.print_progress_bar(i + 1, user_count, prefix='User')

        if book_count:
            for i in range(book_count):
                book = BookFactory()
                book_instances.append(book)
                self.print_progress_bar(i + 1, book_count, prefix='Book')

        if review_count:
            if book_instances and user_instances:
                total_reviews = min(review_count, len(book_instances) * len(user_instances))
                iteration = 0
                for book in book_instances:
                    for user in user_instances:
                        if iteration < review_count:
                            review_instances.append(ReviewFactory(book=book, user=user))
                            iteration += 1
                            self.print_progress_bar(iteration, total_reviews, prefix='Review')
            else:
                self.stdout.write(self.style.WARNING('Please create some users and books first'))

        if bookmark_count:
            if book_instances and user_instances:
                total_bookmarks = min(bookmark_count, len(book_instances) * len(user_instances))
                iteration = 0
                for book in book_instances:
                    for user in user_instances:
                        if iteration < bookmark_count:
                            bookmark_instances.append(BookmarkFactory(book=book, user=user))
                            iteration += 1
                            self.print_progress_bar(iteration, total_bookmarks, prefix='Bookmark')
            else:
                self.stdout.write(self.style.WARNING('Please create some users and books first'))

        for output in user_data_output:
            self.stdout.write(self.style.NOTICE(output))

        self.stdout.write(self.style.SUCCESS('Database seeded successfully'))

    def print_progress_bar(self, iteration, total, prefix='applying', suffix='', length=20):
        """
        Call in a loop to create a terminal progress bar.
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            length      - Optional  : character length of bar (Int)
        """
        percent = 100 * (iteration / float(total))
        filled_length = int(length * iteration // total)
        bar = '⣿' * filled_length + ' ' * (length - filled_length)

        if iteration < total:
            color_start = '\033[94m'
        else:
            color_start = '\033[92m'

        color_end = '\033[0m'

        progress = f'{prefix} [{color_start}{bar}{color_end}] {percent:.1f}% {suffix}'
        self.stdout.write(f'\r{progress}', ending='')
        if iteration == total:
            self.stdout.write('\n')
