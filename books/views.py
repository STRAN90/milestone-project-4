from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Book, Category, Review
from .forms import BookForm, CategoryForm, ReviewForm


def all_books(request):
    """ A view to show all books, including sorting and searching queries """

    books = Book.objects.all()
    query = None
    selected_categories = None
    sort = None
    direction = None
    categories = Category.objects.all() 

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
            selected_categories = request.GET.getlist('category')
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
        'categories': categories,
        'current_categories': selected_categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'books/books.html', context)


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = book.reviews.all()
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.book = book
                review.user = request.user
                review.save()
                return redirect('book_detail', book_id=book.id)
        else:
            return redirect('account_login')

    else:
        form = ReviewForm()

    return render(request, 'books/book_detail.html', {
        'book': book,
        'reviews': reviews,
        'form': form,
    })


@login_required
def add_book(request):
    """ Add a book to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, unauthorised access. Site owner access only')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            messages.success(request, 'Successfully added book!')
            return redirect(reverse('book_detail', args=[book.id]))
        else:
            messages.error(request, 'Failed to add book. Please ensure the form is valid.')
    else:
        form = BookForm()
        
    template = 'books/add_book.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_book(request, book_id):
    """ Edit a book in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, unauthorised access. Site owner access only')
        return redirect(reverse('home'))

    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated book!')
            return redirect(reverse('book_detail', args=[book.id]))
        else:
            messages.error(request, 'Failed to update book. Please ensure the form is valid.')
    else:
        form = BookForm(instance=book)
        messages.info(request, f'You are editing {book.title}')

    template = 'books/edit_book.html'
    context = {
        'form': form,
        'book': book,
    }

    return render(request, template, context)


@login_required
def delete_book(request, book_id):
    """ Delete a book from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, unauthorised access. Site owner access only')
        return redirect(reverse('home'))

    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    messages.success(request, 'Book deleted!')
    return redirect(reverse('books'))


@login_required
def add_category(request):
    """ Add a category to the store"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect(reverse('add_category'))
        else:
            messages.error(
                request, 'Failed to add category. Please ensure the form is valid.')
    else:
        form = CategoryForm()
    template = 'books/add_category.html'
    context = {
        'form': form
    }
    return render(request, template, context)


@login_required
def edit_category(request, category_id):
    """ Edit a category in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, unauthorised access. Site owner access only')
        return redirect(reverse('home'))

    category = get_object_or_404(Category, pk=category_id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated category!')
            return redirect(reverse('add_category'))  # Redirect to appropriate view
        else:
            messages.error(
                request,
                'Failed to update category. Please ensure the form is valid.'
            )
    else:
        form = CategoryForm(instance=category)
        messages.info(request, f'You are editing "{category.friendly_name}"')

    template = 'books/edit_category.html'
    context = {
        'form': form,
        'category': category,
    }

    return render(request, template, context)


@login_required
def delete_category(request, category_id):
    """ Delete a category """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can delete categories.')
        return redirect(reverse('home'))

    category = get_object_or_404(Category, pk=category_id)

    try:
        category.delete()
        messages.success(request, 'Category deleted successfully.')
    except Exception as e:
        messages.error(request, f'An error occurred while deleting the category: {str(e)}')

    # Redirect to add_category page after deletion
    return redirect(reverse('add_category'))


@login_required
def submit_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book = book
            review.save()
            return redirect('book_detail', book_id=book_id)
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'book': book,
    }
    return render(request, 'books/review_submit.html', context)


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('book_detail', book_id=review.book.id)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'books/edit_review.html', {'form': form, 'review': review})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    book_id = review.book.id
    if request.method == 'POST':
        review.delete()
        return redirect('book_detail', book_id=book_id)
    return render(request, 'books/delete_review.html', {'review': review})