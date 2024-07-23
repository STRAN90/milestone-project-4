from django.urls import path
from . import views

urlpatterns = [
    path(
        'add/<int:book_id>/',
        views.add_to_wishlist,
        name='add_to_wishlist'
    ),
    path(
        'view/',
        views.view_wishlist,
        name='view_wishlist'
    ),
    path(
        'remove/<int:book_id>/',
        views.remove_from_wishlist,
        name='remove_from_wishlist'
    ),
]
