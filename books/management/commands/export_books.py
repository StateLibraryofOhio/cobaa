import csv

from django.core.management.base import BaseCommand

from books.models import *


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        file_name = 'export.csv'

        with open(file_name, 'w+', encoding='utf8') as file:
            fieldnames = [
                'award', 'year', 'prize', 'authors', 'title_id', 'title', 'tags'
                ]

            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for award in Award.objects.all():
                authors = ';'.join([author.name for author in award.book.authors.all()])
                tags = ';'.join([tag.tag for tag in award.book.tags.all()])

                writer.writerow({
                    'award': award.award,
                    'year': award.year,
                    'prize': award.prize,
                    'authors': authors,
                    'title_id': award.book.id,
                    'title': award.book.title,
                    'tags': tags,
                    })

        self.stdout.write(self.style.SUCCESS('Data exported successfully'))
