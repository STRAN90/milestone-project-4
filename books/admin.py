from django.contrib import admin
from .models import Category, Book


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'friendly_name')
    search_fields = ('name', 'friendly_name')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'price', 'review_count')
    search_fields = ('title', 'author', 'category__name')
    list_filter = ('category', 'price')
    readonly_fields = ('review_count',)
    fieldsets = (
        (None, {
            'fields': ('title', 'author', 'category', 'description', 'price', 'image')
        }),
        ('Additional Info', {
            'fields': ('review_count',)
        }),
    )

