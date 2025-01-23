from rest_framework import viewsets
from .models import Book, Borrow
from .serializers import BookSerializer, BorrowSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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