from django.db import connection
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver

from .models import Book, Author, Tag


def update_book_search_index(book_id):
    """Update FTS5 index for a specific book"""
    with connection.cursor() as cursor:
        cursor.execute("""
                       SELECT bb.id,
                              bb.title || ' ' ||
                              COALESCE(GROUP_CONCAT(ba.name, ' '), '') || ' ' ||
                              COALESCE(GROUP_CONCAT(bt.tag, ' '), '')
                       FROM books_book bb
                                LEFT JOIN books_book_authors bba ON bb.id = bba.book_id
                                LEFT JOIN books_author ba ON bba.author_id = ba.id
                                LEFT JOIN books_book_tags bbt ON bb.id = bbt.book_id
                                LEFT JOIN books_tag bt ON bbt.tag_id = bt.id
                       WHERE bb.id = :book_id
                         AND bb.hidden = 0
                       GROUP BY bb.id, bb.title
                       """, {'book_id': book_id})

        result = cursor.fetchone()
        if result:
            book_id, combined_text = result
            cursor.execute("""
                INSERT OR REPLACE INTO book_search(rowid, combined_text)
                VALUES (:book_id, :text)
            """, {'book_id': book_id, 'text': combined_text})
        else:
            cursor.execute("DELETE FROM book_search WHERE rowid = :book_id", {'book_id': book_id})


@receiver(post_save, sender=Book)
def book_saved(sender, instance, **kwargs):
    update_book_search_index(instance.id)


@receiver(post_delete, sender=Book)
def book_deleted(sender, instance, **kwargs):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM book_search WHERE rowid = :book_id", {'book_id': instance.id})


@receiver(m2m_changed, sender=Book.authors.through)
def book_authors_changed(sender, instance, **kwargs):
    if kwargs.get('action') in ['post_add', 'post_remove', 'post_clear']:
        update_book_search_index(instance.id)


@receiver(m2m_changed, sender=Book.tags.through)
def book_tags_changed(sender, instance, **kwargs):
    if kwargs.get('action') in ['post_add', 'post_remove', 'post_clear']:
        update_book_search_index(instance.id)


@receiver(post_save, sender=Author)
def author_saved(sender, instance, **kwargs):
    book_ids = instance.books.values_list('id', flat=True)
    for book_id in book_ids:
        update_book_search_index(book_id)


@receiver(post_save, sender=Tag)
def tag_saved(sender, instance, **kwargs):
    book_ids = instance.book_set.values_list('id', flat=True)
    for book_id in book_ids:
        update_book_search_index(book_id)
