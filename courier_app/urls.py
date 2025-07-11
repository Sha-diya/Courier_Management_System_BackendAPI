from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PayOrderView,
    RegisterView,
    ProfileView,
    OrderViewSet,
    UserOrderStatusView,
    CustomTokenObtainPairView,
    UserViewSet,
)
from rest_framework_simplejwt.views import TokenRefreshView

# Router for orders
order_router = DefaultRouter()
order_router.register(r'', OrderViewSet, basename='orders')

# Router for user management (admin only)
user_router = DefaultRouter()
user_router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('orders/status/', UserOrderStatusView.as_view(), name='user_order_status'),
    path('orders/', include(order_router.urls)),
    path('orders/<int:order_id>/pay/', PayOrderView.as_view(), name='pay_order'),

    # Admin user management endpoints
    path('', include(user_router.urls)),
]
