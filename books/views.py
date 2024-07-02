from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Book, Category

def all_books(request):
    """ A view to show all books, including sorting and searching queries """

    books = Book.objects.all()
    query = None
    selected_categories = None
    sort = None
    direction = None
    categories = Category.objects.all()  # Fetch all categories initially

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_title'
                books = books.annotate(lower_title=Lower('title'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if sortkey == 'rating':
                sortkey = 'rating'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            books = books.order_by(sortkey)

        if 'category' in request.GET:
            selected_categories = request.GET['category'].split(',')
            books = books.filter(category__name__in=selected_categories)
            selected_categories = Category.objects.filter(name__in=selected_categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('books'))
            
            queries = Q(title__icontains=query) | Q(description__icontains=query)
            books = books.filter(queries)

    current_sorting = f'{sort}_{direction}' if sort and direction else None

    context = {
        'books': books,
        'search_term': query,
        'categories': categories,  # Pass all categories to the template
        'current_categories': selected_categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'books/books.html', context)

def book_detail(request, book_id):
    """ A view to show individual book details """
    book = get_object_or_404(Book, pk=book_id)

    context = {
        'book': book,
    }

    return render(request, 'books/book_detail.html', context)
