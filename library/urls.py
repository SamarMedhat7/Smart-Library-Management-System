from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BorrowViewSet,user_dashboard,create_payment,payment_success, payment_cancel

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'borrows', BorrowViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('dashboard', user_dashboard, name='user_dashboard_api'),
    path('create-payment/<int:borrow_id>/', create_payment, name='create-payment'),
    path('api/success/', payment_success),
    path('api/cancel/', payment_cancel),

]