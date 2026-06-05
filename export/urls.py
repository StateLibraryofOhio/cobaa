from django.urls import path

from . import views

app_name = 'export'

urlpatterns = [
    path('', views.books_to_excel, name='books_to_excel'),
    ]
