from rest_framework import viewsets
from .models import Book, Borrow
from .serializers import BookSerializer, BorrowSerializer
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from paypalrestsdk import configure, Payment
from django.conf import settings
from django.shortcuts import get_object_or_404
import logging
import re

logger = logging.getLogger(__name__)

# PayPal configuration
configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    
    @action(detail=False, methods=['get'])
    def search_books(self,request):
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

        return Response({
        'count': books.count(),
        'results': serializer.data
            })    


    @action(detail=False, methods=['get'])
    def search_suggestions(self,request):
        query = request.GET.get('q', '')
        suggestions = []

        if query:
            suggestions = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query)).distinct()[:5]

        suggestion_data = [{'title': book.title, 'author': book.author} for book in suggestions]

        return Response(suggestion_data)
    

class BorrowViewSet(viewsets.ModelViewSet):
    serializer_class = BorrowSerializer
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Borrow.objects.all()
        return Borrow.objects.filter(user=user)

    

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




@api_view(['POST'])
@permission_classes([IsAuthenticated])

def create_payment(request,borrow_id):
    borrow = get_object_or_404(Borrow, id=borrow_id, user=request.user)

    payment = Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
       "redirect_urls": {
            "return_url": request.build_absolute_uri("/api/success/"),
            "cancel_url": request.build_absolute_uri("/api/cancel/")
        },
        "transactions": [{
            "amount": {
                "total": str(borrow.fine), 
                "currency": "USD"
            },
        "description": f"Payment for borrow ID {borrow.id} by user ID {request.user.id}"    }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                return Response({'approval_url': link.href})

    else:
        logger.error("PayPal payment creation failed: %s", payment.error)
        return Response({'error': payment.error}, status=400)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_success(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    try:
        payment = Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
        # Extract borrow_id and user_id from description
            description = payment.transactions[0].description
            import re
            match = re.search(r"ID (\d+) by user ID (\d+)", description)
            if not match:
                return Response({'error': 'Invalid payment description'}, status=400)

            borrow_id = int(match.group(1))
            user_id = int(match.group(2))

            if user_id != request.user.id:
                return Response({'error': 'Unauthorized access'}, status=403)

        
            borrow = get_object_or_404(Borrow, id=borrow_id, user=request.user)
            borrow.fine = 0
            borrow.save()
            return Response({'status': 'Payment successful, fine cleared'})
        else:
            logger.error("PayPal payment execution failed: %s", payment.error)
            return Response({'error': payment.error}, status=400)
    except Exception as e:
        logger.exception("Unexpected error during PayPal success callback")
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET'])
def payment_cancel(request):
    return Response({'status': 'Payment cancelled'})
