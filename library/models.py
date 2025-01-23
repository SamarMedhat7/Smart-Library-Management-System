from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    publication_year = models.IntegerField()
    is_available = models.BooleanField(default=True)
    rating = models.FloatField(default=0.0)

class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned = models.BooleanField(default=False)
    fine = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)