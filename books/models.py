from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import truncatewords
from django.urls import reverse


class Tag(models.Model):
    tag = models.CharField('Tags', max_length=35, unique=True)

    class Meta:
        ordering = ['tag']

    def __str__(self):
        return self.tag


class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class BookManager(models.Manager):
    def get_queryset(self):
        return super(BookManager, self).get_queryset().filter(hidden=0)


class Book(models.Model):
    title = models.CharField('Book Title', max_length=250)
    authors = models.ManyToManyField(Author, related_name='books')
    tags = models.ManyToManyField(Tag, verbose_name='tags', blank=True)
    hidden = models.BooleanField(default=False, verbose_name='Hidden from search results')

    def get_absolute_url(self):
        return reverse('books:book_list', args=[self.id])

    objects = models.Manager()
    published = BookManager()

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class AwardQuerySet(models.query.QuerySet):
    def published(self):
        return self.filter(hidden=False)


class AwardManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return AwardQuerySet(self.model)

    def published(self, *args, **kwargs):
        return self.get_queryset().published(*args, **kwargs)


class Award(models.Model):
    award = models.CharField(max_length=75,
                             choices=[
                                 ('a', 'Ansfield-Wolf'),
                                 ('b', 'Buckeye Children\'s & Teen'),
                                 ('c', 'Choose to Read Ohio'),
                                 ('d', 'Dayton Literary Peace Prize'),
                                 ('f', 'Floyd\'s Pick'),
                                 ('j', 'James Cook'),
                                 ('n', 'Norman A. Sugarman'),
                                 ('o', 'Ohioana'),
                                 ('t', 'Thurber Prize')
                                 ])
    year = models.SmallIntegerField(validators=[MinValueValidator(1900, message="Invalid date"),
                                                MaxValueValidator(date.today().year + 1, message="Invalid date")])
    prize = models.CharField(max_length=1,
                             choices=(
                                 ('c', 'Featured Title'),
                                 ('f', 'Finalist'),
                                 ('h', 'Honor'),
                                 ('m', 'Honorable Mention'),
                                 ('n', 'Nominee'),
                                 ('r', 'Runner-Up'),
                                 ('s', 'Special Honor'),
                                 ('w', 'Winner'),
                                 ),
                             verbose_name="Prize")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='awards')
    hidden = models.BooleanField(default=False, verbose_name='Hidden from search results')

    @property
    def get_short_book_title(self):
        return truncatewords(self.book.title, 10)

    @property
    def get_authors(self):
        return ' & '.join([author.name for author in self.book.authors.all()])

    objects = AwardManager()

    class Meta:
        ordering = ['award', '-year']

    def __str__(self):
        return f'{self.year} {self.get_award_display()} - {self.get_prize_display()}'
