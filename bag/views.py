from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from books.models import Book
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def view_bag(request):
    """A view that renders the bag contents page"""
    return render(request, 'bag/bag.html')

@login_required
def add_to_bag(request, item_id):
    """Add a quantity of the specified product to the shopping bag"""
    book = get_object_or_404(Book, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
        messages.success(request, f'Updated {book.title} quantity to {bag[item_id]}')
    else:
        bag[item_id] = quantity
        messages.success(request, f'Added {book.title} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)

@login_required
def adjust_bag(request, item_id):
    """Adjust quantity of the book to the specified amount"""
    book = get_object_or_404(Book, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    bag = request.session.get('bag', {})

    if quantity > 99:
        messages.error(request, 'Sorry, value must be less than or equal to 99.')
    elif quantity > 0:
        bag[item_id] = quantity
        messages.success(request, f'Updated {book.title} quantity to {bag[item_id]}')
    else:
        bag.pop(item_id)
        messages.success(request, f'Removed {book.title} from your bag')

    request.session['bag'] = bag
    return redirect(reverse("view_bag"))

@login_required
def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""
    try:
        book = get_object_or_404(Book, pk=item_id)
        bag = request.session.get('bag', {})

        if item_id in bag:
            bag.pop(item_id)
            messages.success(request, f'Removed {book.title} from your shopping bag')
        else:
            messages.error(request, f'Item {book.title} not found in your shopping bag')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)