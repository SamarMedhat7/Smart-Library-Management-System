from rest_framework import viewsets
from .models import Book, Borrow
from .serializers import BookSerializer, BorrowSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BorrowViewSet(viewsets.ModelViewSet):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_dashboard(request):
    user_borrows = Borrow.objects.filter(user=request.user)
    serializer = BorrowSerializer(user_borrows, many=True)
    
    total_fine = sum(borrow.fine for borrow in user_borrows if not borrow.returned)

    return Response({
        'borrowing_history': serializer.data,
        'total_fine': total_fine,
    })    



@api_view(['GET'])
def search_books(request):
    query = request.GET.get('q', '')
    availability = request.GET.get('availability', None)
    publication_year = request.GET.get('publication_year', None)
    rating = request.GET.get('rating', None)
    genres = request.GET.getlist('genres', [])
    authors = request.GET.getlist('authors', [])

    filters = Q()

    if query:
        filters &= Q(title__icontains=query) | Q(author__icontains=query) | Q(genre__icontains=query)

    if availability is not None:
        filters &= Q(is_available=availability.lower() == 'true')

    if publication_year:
        filters &= Q(publication_year=publication_year)

    if rating:
        filters &= Q(rating__gte=rating)

    if genres:
        filters &= Q(genre__in=genres)

    if authors:
        filters &= Q(author__in=authors)
    books = Book.objects.filter(filters)
    serializer = BookSerializer(books, many=True)

    return Response(serializer.data)    


@api_view(['GET'])
def search_suggestions(request):
    query = request.GET.get('q', '')
    suggestions = []

    if query:
        suggestions = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query)).distinct()[:5]

    suggestion_data = [{'title': book.title, 'author': book.author} for book in suggestions]

    return Response(suggestion_data)