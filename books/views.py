from django.shortcuts import (
    render,
    redirect,
    reverse,
    get_object_or_404
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Book, Category, Review
from .forms import BookForm, CategoryForm, ReviewForm


def all_books(request):
    """View to display all books with filtering,
    sorting, and search options."""
    books = Book.objects.all()
    query = None
    selected_categories = None
    sort = None
    direction = None
    categories = Category.objects.all()
    current_sorting = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_title'
                books = books.annotate(lower_title=Lower('title'))
            elif sortkey == 'category':
                sortkey = 'category__name'
            elif sortkey == 'rating':
                sortkey = 'rating'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            books = books.order_by(sortkey)

        if 'category' in request.GET:
            selected_categories = request.GET.getlist('category')
            books = books.filter(
                category__name__in=selected_categories
            )
            selected_categories = Category.objects.filter(
                name__in=selected_categories
            )

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('books'))

            queries = Q(
                title__icontains=query) | Q(description__icontains=query)
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
    """View to display details of a specific book and handle reviews."""
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

    context = {
        'book': book,
        'reviews': reviews,
        'form': form,
    }

    return render(request, 'books/book_detail.html', context)


@login_required
def add_book(request):
    """View to add a new book, restricted to superusers."""
    if not request.user.is_superuser:
        messages.error(
            request,
            'Sorry, unauthorized access. Site owner access only'
        )
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            messages.success(request, 'Successfully added book!')
            return redirect(reverse('book_detail', args=[book.id]))
        else:
            messages.error(
                request,
                'Failed to add book. Please ensure the form is valid.'
            )
    else:
        form = BookForm()

    context = {
        'form': form,
    }

    return render(request, 'books/add_book.html', context)


@login_required
def edit_book(request, book_id):
    """View to edit an existing book, restricted to superusers."""
    if not request.user.is_superuser:
        messages.error(
            request,
            'Sorry, unauthorized access. Site owner access only'
        )
        return redirect(reverse('home'))

    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated book!')
            return redirect(reverse('book_detail', args=[book.id]))
        else:
            messages.error(
                request,
                'Failed to update book. Please ensure the form is valid.'
            )
    else:
        form = BookForm(instance=book)
        messages.info(request, f'You are editing {book.title}')

    context = {
        'form': form,
        'book': book,
    }

    return render(request, 'books/edit_book.html', context)


@login_required
def delete_book(request, book_id):
    """View to delete a specific book, restricted to superusers."""
    if not request.user.is_superuser:
        messages.error(
            request,
            'Sorry, unauthorized access. Site owner access only'
        )
        return redirect(reverse('home'))

    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    messages.success(request, 'Book deleted!')
    return redirect(reverse('books'))


@login_required
def add_category(request):
    """View to add a new category."""
    if not request.user.is_superuser:
        messages.error(
            request,
            'You do not have permission to add a category.'
        )
        return redirect('some_other_view')  # Redirect to an appropriate view

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect(reverse('add_category'))
        else:
            messages.error(
                request,
                'Failed to add category. Please ensure the form is valid.'
            )
    else:
        form = CategoryForm()

    context = {
        'form': form,
    }

    return render(request, 'books/add_category.html', context)


@login_required
def edit_category(request, category_id):
    """View to edit an existing category, restricted to superusers."""
    if not request.user.is_superuser:
        messages.error(
            request,
            'Sorry, unauthorized access. Site owner access only'
        )
        return redirect(reverse('home'))

    category = get_object_or_404(Category, pk=category_id)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated category!')
            return redirect(reverse('add_category'))
        else:
            messages.error(
                request,
                'Failed to update category. Please ensure the form is valid.'
            )
    else:
        form = CategoryForm(instance=category)
        messages.info(request, f'You are editing "{category.friendly_name}"')

    context = {
        'form': form,
        'category': category,
    }

    return render(request, 'books/edit_category.html', context)


@login_required
def delete_category(request, category_id):
    """View to delete a category, restricted to superusers."""
    if not request.user.is_superuser:
        messages.error(
            request,
            'Sorry, only store owners can delete categories.'
        )
        return redirect(reverse('home'))

    category = get_object_or_404(Category, pk=category_id)

    try:
        category.delete()
        messages.success(request, 'Category deleted successfully.')
    except Exception as e:
        messages.error(
            request,
            f'An error occurred while deleting the category: {str(e)}'
        )

    return redirect(reverse('add_category'))


@login_required
def submit_review(request, book_id):
    """View to submit a review for a book."""
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
    """View to edit a review, restricted to the review's author."""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('book_detail', book_id=review.book.id)
    else:
        form = ReviewForm(instance=review)

    return render(
        request,
        'books/edit_review.html',
        {'form': form, 'review': review}
    )


@login_required
def delete_review(request, review_id):
    """View to delete a review, restricted to the review's author."""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    book_id = review.book.id
    if request.method == 'POST':
        review.delete()
        return redirect('book_detail', book_id=book_id)
    return render(request, 'books/delete_review.html', {'review': review})


def clearance_books(request):
    """View to display books on clearance."""
    books = Book.objects.filter(is_clearance=True)
    return render(request, 'books/clearance_books.html', {'books': books})


def new_arrivals(request):
    """View to display new arrival books."""
    books = Book.objects.filter(is_new_arrival=True).order_by('-created_at')
    return render(request, 'books/new_arrivals.html', {'books': books})
