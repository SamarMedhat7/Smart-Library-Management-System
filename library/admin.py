from django.contrib import admin
from .models import Book, Borrow

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'publication_year', 'is_available', 'rating')
    list_filter = ('genre', 'is_available', 'publication_year')
    search_fields = ('title', 'author')


@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrow_date', 'due_date', 'returned', 'fine')
    list_filter = ('returned', 'due_date')
    search_fields = ('user__username', 'book__title')
    actions = ['mark_returned']

    @admin.action(description='Mark selected as returned')
    def mark_returned(self, request, queryset):
        queryset.update(returned=True)
