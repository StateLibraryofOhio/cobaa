from books.models import Award, Book


def test_book_str(book):
    assert str(book) == 'The Great Test Book'


def test_published_manager_excludes_hidden(book, hidden_book):
    assert list(Book.published.all()) == [book]
    assert Book.objects.count() == 2


def test_award_str(book):
    assert str(book.awards.get()) == '2020 Ohio Book Award - Winner'


def test_award_published_excludes_hidden(book):
    Award.objects.create(award='o', year=2021, prize='f', book=book, hidden=True)
    assert Award.objects.published().count() == 1


def test_award_authors_property(book):
    assert book.awards.get().get_authors == 'Jane Author'
