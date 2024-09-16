from django.contrib import admin

from .models.book import Book
from .models.bookmark import Bookmark
from .models.review import Review


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 2


class BookmarkInline(admin.TabularInline):
    model = Bookmark
    extra = 2


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'bookmark_count', 'review_count', 'average_rating')
    search_fields = ('title',)
    readonly_fields = ('bookmark_count', 'review_count', 'average_rating', 'rating_distribution')
    inlines = [ReviewInline, BookmarkInline]

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

    def average_rating(self, obj):
        from .services.queries.review import average_rating
        return average_rating(book=obj)

    def rating_distribution(self, obj):
        from .services.queries.review import rating_distribution
        return rating_distribution(book=obj)

    bookmark_count.short_description = 'Bookmark Count'
    review_count.short_description = 'Review Count'
    average_rating.short_description = 'Average Rating'
    rating_distribution.short_description = 'Rating Distribution'


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
