from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    """Category model to classify cookbooks."""

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Book(models.Model):
    """Book model to store details about individual cookbooks."""

    FORMAT_CHOICES = [
        ('HB', 'Hardback'),
        ('PB', 'Paperback'),
    ]

    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    title = models.CharField(max_length=254)
    author = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    rating = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )
    review_count = models.PositiveIntegerField(default=0)
    format = models.CharField(
        max_length=2,
        choices=FORMAT_CHOICES,
        default='PB'
    )
    is_clearance = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    """Review model to store user reviews for cookbooks."""

    book = models.ForeignKey(
        Book,
        related_name='reviews',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        related_name='reviews',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=254)
    content = models.TextField()
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1
    )  # Ratings out of 5.0
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.user.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_book_rating()

    def update_book_rating(self):
        """Update the book's rating based on its reviews."""
        reviews = self.book.reviews.all()
        self.book.review_count = reviews.count()
        total_rating = sum(review.rating for review in reviews)
        self.book.rating = (
            total_rating / self.book.review_count
            if self.book.review_count > 0
            else 0
        )
        self.book.save()


class Wishlist(models.Model):
    """Wishlist model to store user's wishlists of cookbooks."""

    user = models.ForeignKey(
        User,
        related_name='wishlists',
        on_delete=models.CASCADE
    )
    books = models.ManyToManyField(
        Book,
        related_name='wishlists'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist of {self.user.username}"
