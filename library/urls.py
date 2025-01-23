from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BorrowViewSet,user_dashboard

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'borrows', BorrowViewSet)
router.register(r'borrows', BorrowViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('dashboard', user_dashboard, name='user_dashboard_api'),
]