from django.urls import path

from . import views

app_name = 'pdf'

urlpatterns = [
    path('export/', views.books_to_pdf, name='books_to_pdf'),
    ]
