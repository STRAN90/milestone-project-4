from django.contrib import admin
from .models import Category, Book, Review, Wishlist


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'friendly_name')
    search_fields = ('name', 'friendly_name')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'price', 'review_count', 'format', 'is_clearance', 'is_new_arrival')
    search_fields = ('title', 'author', 'category__name')
    list_filter = ('category', 'price', 'is_clearance', 'is_new_arrival')
    readonly_fields = ('review_count', 'created_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'author', 'category', 'description', 'price', 'image', 'format')
        }),
        ('Additional Info', {
            'fields': ('review_count', 'is_clearance', 'is_new_arrival', 'created_at')
        }),
    )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'book', 'user', 'rating', 'created_at')
    search_fields = ('title', 'book__title', 'user__username')
    list_filter = ('book', 'rating')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)
    filter_horizontal = ('books',)

