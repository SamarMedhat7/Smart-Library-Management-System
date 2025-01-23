from rest_framework import viewsets
from .models import Book, Borrow
from .serializers import BookSerializer, BorrowSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BorrowViewSet(viewsets.ModelViewSet):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer