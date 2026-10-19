from django.db import migrations

# The FTS5 table backing keyword search (see books/signals.py and books/filters.py).
# Production already has this table, so creation is idempotent; the definition must
# match what is deployed. Reverse is a no-op so a rollback never drops the live index.
CREATE_BOOK_SEARCH = """
    CREATE VIRTUAL TABLE IF NOT EXISTS book_search USING fts5(
        combined_text,
        tokenize='porter'
    )
"""


class Migration(migrations.Migration):
    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(CREATE_BOOK_SEARCH, reverse_sql=migrations.RunSQL.noop),
    ]
