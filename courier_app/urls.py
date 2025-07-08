from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PayOrderView
from .views import RegisterView, ProfileView, OrderViewSet, UserOrderStatusView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'', OrderViewSet, basename='orders')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('orders/status/', UserOrderStatusView.as_view(), name='user_order_status'),
    path('orders/', include(router.urls)),
    path('orders/<int:order_id>/pay/', PayOrderView.as_view(), name='pay_order'),
]
