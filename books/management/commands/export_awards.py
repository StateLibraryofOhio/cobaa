import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Case, Value, CharField, When
from openpyxl import Workbook

from books.models import Award


class Command(BaseCommand):
    help = 'Export awards to an Excel file (Complete Awards List.xlsx)'

    def handle(self, *args, **options):
        file_name = getattr(settings, 'BASE_DIR', os.getcwd())
        file_path = os.path.join(file_name, 'Complete Awards List.xlsx')

        wb = Workbook()
        ws = wb.active
        ws.title = 'Awards'

        # Define headers
        headers = ['Award', 'Year', 'Prize', 'Title', 'Authors', 'Tags']
        ws.append(headers)

        # Create Case expression dynamically from choices
        award_choices = Award._meta.get_field('award').choices
        award_cases = [When(award=code, then=Value(name)) for code, name in award_choices]

        # Query: exclude hidden awards and hidden books/titles, sort by award display name, year, title
        qs = Award.objects.filter(
            hidden=False,
            book__hidden=False
        ).select_related('book').prefetch_related(
            'book__authors',
            'book__tags'
        ).annotate(
            award_display_name=Case(
                *award_cases,
                default=Value(''),
                output_field=CharField(),
            )
        ).order_by('award_display_name', 'year', 'book__title')

        for award in qs:
            book = award.book

            # Join authors with comma
            authors = ', '.join([author.name for author in book.authors.all()])

            # Join tags with comma
            tags = ', '.join([tag.tag for tag in book.tags.all()])

            row = [
                award.get_award_display(),
                award.year,
                award.get_prize_display(),
                book.title,
                authors,
                tags,
            ]

            ws.append(row)

        # Make headers filterable
        ws.auto_filter.ref = ws.dimensions

        # Auto-adjust column widths
        for column_cells in ws.columns:
            length = max((len(str(cell.value)) for cell in column_cells), default=0)
            col_letter = column_cells[0].column_letter
            ws.column_dimensions[col_letter].width = min(max(length + 2, 10), 60)

        # Freeze the header row
        ws.freeze_panes = 'A2'

        wb.save(file_path)
        self.stdout.write(
            self.style.SUCCESS(f'Awards exported successfully to {file_path}')
        )
