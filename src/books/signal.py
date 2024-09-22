from django.db.models.signals import post_save
from django.dispatch import receiver

from books.models import Review

# TODO : it should be configurable env.int(...)
threshold = 20


@receiver(post_save, sender=Review)
def calculate_stats_signal(sender, instance, created, **kwargs):
    from books.models import BookStat
    from django.core.cache import cache
    cache_key = f"pending_stats_{instance.book.id}"

    pending_stats = cache.get(cache_key, 0)
    pending_stats += 1
    cache.set(cache_key, pending_stats, timeout=None)

    if pending_stats >= threshold:
        BookStat.update_or_create_stat(book=instance.book)
        instance.book.save()
        instance.book.stat.save()
        cache.set(cache_key, 0, timeout=None)
