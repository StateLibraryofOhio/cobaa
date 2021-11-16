import csv

from django.core.management.base import BaseCommand

from books.models import *


class Command(BaseCommand):
    """
    Example import file should look like:

    award,year,prize,authors,title_id,title,tags
    o,2002,w,"Longaberger, Dave;Longaberger, Tami",1443,Longaberger: An American Success Story,Head Award

    Titles without an id will be assigned a new one.

    """

    def add_arguments(self, parser):
        parser.add_argument(
            'file_name', type=str, help='The CSV file that contains book award entries.')

    def handle(self, *args, **kwargs):
        file_name = kwargs['file_name']
        with open(file_name, encoding='utf8') as file:
            reader = csv.DictReader(file, skipinitialspace=True)

            for row in reader:

                for author in row['authors'].split(';'):
                    author, created = Author.objects.get_or_create(
                        name=author
                        )

                    author.save()

                # If incoming id is empty, assign a new book id
                book_id = row['title_id'] if row['title_id'] != '' \
                    else Book.objects.latest('id').id + 1

                book, created = Book.objects.get_or_create(
                    id=book_id,
                    title=row['title']
                    )

                if created:
                    book.save()

                for author in row['authors'].split(';'):
                    book.authors.add(
                        Author.objects.get(name=author)
                        )

                book.save()

                for tag in row['tags'].split(';'):
                    tag, created = Tag.objects.get_or_create(tag=tag)
                    book.tags.add(
                        Tag.objects.get(tag=tag)
                        )

                award, created = Award.objects.get_or_create(
                    award=row['award'],
                    year=row['year'],
                    prize=row['prize'],
                    book=book
                    )

                award.save()

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
