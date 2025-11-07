import os
import tempfile

from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from django.core.management.base import BaseCommand
from django.db.models import Case, Value, CharField, When
from openpyxl import Workbook

from books.models import Award


class Command(BaseCommand):
    help = 'Export awards to an Excel file and upload to Cloudinary'

    def handle(self, *args, **options):
        # Create a temporary file for the Excel data
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
            temp_file_path = temp_file.name

        try:
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

            # Save to temporary file
            wb.save(temp_file_path)

            # Upload to Cloudinary
            self.stdout.write("Uploading file to Cloudinary...")

            upload_result = upload(
                temp_file_path,
                public_id="lsta/cobaa/Complete_Awards_List",
                resource_type="raw",
                overwrite=True,
                format="xlsx"
            )

            # Use the secure_url directly from upload result
            public_url = upload_result['secure_url']

            self.stdout.write(
                self.style.SUCCESS(f'Awards exported successfully to Cloudinary')
            )
            self.stdout.write(
                self.style.SUCCESS(f'Public URL: {public_url}')
            )

        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
