from django.forms import ValidationError
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import stripe
import logging

from .models import User, Order
from .serializers import RegisterSerializer, UserSerializer, OrderSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)


# Register endpoint
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


# User profile endpoint
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


# Custom permissions
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.Roles.ADMIN


class IsDeliveryMan(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.Roles.DELIVERY_MAN


class IsOrderOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class UserOrderStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        orders = Order.objects.filter(user=user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing orders:
    - Admin: full access.
    - Delivery Man: can view assigned orders and update order status.
    - User: can create and view own orders.
    """
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Roles.ADMIN:
            return Order.objects.all()
        elif user.role == User.Roles.DELIVERY_MAN:
            return Order.objects.filter(delivery_man=user)
        else:  # regular user
            return Order.objects.filter(user=user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            # Only Admin or Delivery man allowed to update/destroy orders
            if self.request.user.role == User.Roles.ADMIN:
                return [permissions.IsAuthenticated()]
            elif self.request.user.role == User.Roles.DELIVERY_MAN:
                return [permissions.IsAuthenticated()]
            else:
                # Regular users cannot update or delete orders
                return [permissions.IsAdminUser()]  # effectively deny access
        elif self.action == 'create':
            return [permissions.IsAuthenticated()]
        elif self.action == 'assigned':
            # Only delivery men can access assigned orders explicitly
            return [permissions.IsAuthenticated(), IsDeliveryMan()]
        else:
            # list, retrieve allowed for authenticated users
            return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        # Save order with user set
        order = serializer.save(user=self.request.user)

        # Validate total_amount presence and positive value
        if order.total_amount is None:
            raise ValidationError({"total_amount": "Total amount is required."})

        if order.total_amount <= 0:
            raise ValidationError({"total_amount": "Total amount must be greater than 0."})

        # Optional payment on creation
        pay_now = self.request.data.get('pay_now', False)
        if pay_now in [True, 'true', 'True', '1', 1]:
            try:
                intent = stripe.PaymentIntent.create(
                    amount=int(order.total_amount * 100),  # dollars to cents
                    currency='usd',
                    metadata={'order_id': order.id},
                    automatic_payment_methods={'enabled': True},
                )
                order.stripe_payment_intent = intent.id
                order.payment_method = 'stripe'
                order.save()

                # Attach client_secret for frontend payment
                self.extra_context = {'client_secret': intent.client_secret}

            except stripe.error.StripeError as e:
                logger.error(f"Stripe error on order creation payment intent: {e}")

        # No explicit return needed — DRF handles response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # Add client_secret to response if payment intent created
        if hasattr(self, 'extra_context') and 'client_secret' in self.extra_context:
            response.data['client_secret'] = self.extra_context['client_secret']
        return response

    def update(self, request, *args, **kwargs):
        order = self.get_object()

        if request.user.role == User.Roles.DELIVERY_MAN:
            if order.delivery_man != request.user:
                return Response({"detail": "You are not assigned to this order."}, status=status.HTTP_403_FORBIDDEN)

            # Delivery man can only update the status field
            status_field = request.data.get('status')
            if status_field not in dict(Order.StatusChoices.choices):
                return Response({"detail": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

            order.status = status_field
            order.save()
            serializer = self.get_serializer(order)
            return Response(serializer.data)

        elif request.user.role == User.Roles.ADMIN:
            # Admin can update any fields
            return super().update(request, *args, **kwargs)

        else:
            return Response({"detail": "You do not have permission to update this order."}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['get'])
    def assigned(self, request):
        """
        Custom endpoint for delivery men to view their assigned orders.
        URL: /api/v1/orders/assigned/
        """
        if request.user.role != User.Roles.DELIVERY_MAN:
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)

        orders = Order.objects.filter(delivery_man=request.user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)


class PayOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)

            if order.is_paid:
                return Response({"message": "Order already paid."}, status=status.HTTP_400_BAD_REQUEST)

            amount = int(order.total_amount * 100)  # convert dollars to cents
            if amount <= 0:
                return Response({"error": "Invalid order amount."}, status=status.HTTP_400_BAD_REQUEST)

            # Reuse existing PaymentIntent if available
            if order.stripe_payment_intent:
                intent = stripe.PaymentIntent.retrieve(order.stripe_payment_intent)
            else:
                intent = stripe.PaymentIntent.create(
                    amount=amount,
                    currency='usd',
                    metadata={'order_id': str(order.id)},
                    automatic_payment_methods={'enabled': True},
                )
                order.stripe_payment_intent = intent.id
                order.payment_method = 'stripe'
                order.save()

            return Response({
                'client_secret': intent.client_secret
            }, status=status.HTTP_200_OK)

        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        except stripe.error.StripeError as e:
            logger.error(f"Stripe error during payment intent retrieval/creation: {e}")
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        except Exception as e:
            logger.error(f"Unexpected error in PayOrderView: {e}")
            return Response({"error": "Something went wrong."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
