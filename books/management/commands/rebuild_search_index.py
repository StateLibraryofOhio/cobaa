from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Rebuild the FTS5 search index from scratch'

    def add_arguments(self, parser):
        parser.add_argument(
            '--verify',
            action='store_true',
            help='Verify index after rebuild',
        )

    def handle(self, *args, **options):
        self.stdout.write('Rebuilding search index...')

        with connection.cursor() as cursor:
            # Clear existing index
            cursor.execute("DELETE FROM book_search")
            self.stdout.write('Cleared existing index')

            # Rebuild from scratch
            cursor.execute("""
                           INSERT INTO book_search(rowid, combined_text)
                           SELECT bb.id,
                                  bb.title || ' ' ||
                                  COALESCE(GROUP_CONCAT(ba.name, ' '), '') || ' ' ||
                                  COALESCE(GROUP_CONCAT(bt.tag, ' '), '')
                           FROM books_book bb
                                    LEFT JOIN books_book_authors bba ON bb.id = bba.book_id
                                    LEFT JOIN books_author ba ON bba.author_id = ba.id
                                    LEFT JOIN books_book_tags bbt ON bb.id = bbt.book_id
                                    LEFT JOIN books_tag bt ON bbt.tag_id = bt.id
                           WHERE bb.hidden = 0
                           GROUP BY bb.id, bb.title
                           """)

            # Get count
            cursor.execute("SELECT COUNT(*) FROM book_search")
            count = cursor.fetchone()[0]

        self.stdout.write(self.style.SUCCESS(f'Search index rebuilt: {count} books indexed'))

        if options['verify']:
            self.verify_index()

    def verify_index(self):
        """Verify the index is working"""
        self.stdout.write('Verifying index...')
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM books_book WHERE hidden = 0")
            book_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM book_search")
            index_count = cursor.fetchone()[0]

            if book_count == index_count:
                self.stdout.write(self.style.SUCCESS(f'✓ Index verified: {book_count} books'))
            else:
                self.stdout.write(self.style.WARNING(
                    f'⚠ Mismatch: {book_count} books but {index_count} indexed'
                ))
