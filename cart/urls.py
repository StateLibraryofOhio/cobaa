from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:book_id>/', views.cart_add, name='cart_add'),
    path('clear/', views.cart_clear, name='cart_clear'),
    path('export/', views.cart_export, name='cart_export'),
    path('remove/<int:book_id>/', views.cart_remove, name='cart_remove'),
    path('retrieve/', views.cart_retrieve, name='cart_retrieve'),
    path('total/', views.cart_total, name='cart_total'),
    path('update/<int:book_id>/', views.cart_update, name='cart_update'),
    ]
