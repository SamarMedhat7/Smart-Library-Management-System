from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BorrowViewSet,user_dashboard,search_books,search_suggestions

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'borrows', BorrowViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('dashboard', user_dashboard, name='user_dashboard_api'),
    path('books/search/', search_books, name='search_books'),
    path('api/books/suggestions/', search_suggestions, name='search_suggestions'),

]