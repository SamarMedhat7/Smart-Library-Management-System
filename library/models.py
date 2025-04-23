from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    publication_year = models.IntegerField()
    is_available = models.BooleanField(default=True)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.title

class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned = models.BooleanField(default=False)
    fine = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

    def update_fine(self):
        if not self.returned:
            overdue_days = (timezone.now().date() - self.due_date).days
            if overdue_days > 0:
                self.fine = overdue_days * 1.00  # $1 per day fine
                self.save()