from django.contrib import admin

from .models.book import Book
from .models.bookmark import Bookmark
from .models.review import Review


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'bookmark_count', 'review_count', 'average_rating')
    search_fields = ('title',)
    readonly_fields = ('bookmark_count', 'review_count', 'average_rating', 'rating_distribution')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        return []

    def bookmark_count(self, obj):
        from .services.queries.bookmark import bookmark_count
        return bookmark_count(book=obj)

    def review_count(self, obj):
        from .services.queries.review import review_count
        return review_count(book=obj)

    bookmark_count.short_description = 'Bookmark Count'
    review_count.short_description = 'Review Count'


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('book', 'user')
    search_fields = ('book__title', 'user__email')
    list_filter = ('book', 'user')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'comment')
    search_fields = ('book__title', 'user__email', 'comment')
    list_filter = ('rating', 'book', 'user')
