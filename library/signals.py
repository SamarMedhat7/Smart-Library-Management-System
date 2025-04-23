from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Borrow, Book

@receiver(post_save, sender=Borrow)
def update_book_availability(sender, instance, **kwargs):
    book = instance.book
    if instance.returned:
        book.is_available = True
    else:
        book.is_available = False
    book.save()
