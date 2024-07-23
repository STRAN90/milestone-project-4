from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from books.models import Book
from .models import Wishlist


@login_required
def add_to_wishlist(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, book=book)
    if created:
        messages.success(request, 'Book added to your wishlist!')
    else:
        messages.info(request, 'Book is already in your wishlist.')
    return redirect('view_wishlist')


@login_required
def view_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, 'wishlist/view_wishlist.html', context)


@login_required
def remove_from_wishlist(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    wishlist = get_object_or_404(Wishlist, user=request.user, book=book)
    wishlist.delete()
    messages.success(request, 'Book removed from your wishlist!')
    return redirect('view_wishlist')
