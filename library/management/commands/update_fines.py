from django.core.management.base import BaseCommand
from library.models import Borrow
from django.utils import timezone
from library.utils import send_fine_notification

class Command(BaseCommand):
    help = 'Update fines for overdue books and send notifications'

    def handle(self, *args, **kwargs):
        borrows = Borrow.objects.filter(returned=False, due_date__lt=timezone.now())
        for borrow in borrows:
            borrow.update_fine()
            send_fine_notification(borrow.user, borrow)
            self.stdout.write(self.style.SUCCESS(f'Notification sent for {borrow.book.title}'))