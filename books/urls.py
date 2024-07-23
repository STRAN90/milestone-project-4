from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_books, name='books'),
    path('add/', views.add_book, name='add_book'),
    path('edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('<int:book_id>/', views.book_detail, name='book_detail'),
    path('add_category/', views.add_category, name='add_category'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('review/edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('clearance/', views.clearance_books, name='clearance_books'),
    path('new-arrivals/', views.new_arrivals, name='new_arrivals'),
]