from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        DELIVERY_MAN = "DELIVERY_MAN", "Delivery Man"
        USER = "USER", "User"

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.USER,
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
    

class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PICKED = "PICKED", "Picked"
        IN_TRANSIT = "IN_TRANSIT", "In Transit"
        RETURNED = "RETURNED", "Returned"
        DELIVERED = "DELIVERED", "Delivered"
        COMPLETE = "COMPLETE", "Complete"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    delivery_man = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_orders')
    pickup_address = models.CharField(max_length=255)
    delivery_address = models.CharField(max_length=255)
    package_details = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    stripe_payment_intent = models.CharField(max_length=255, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    payment_method = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="e.g., 'card', 'cash', 'stripe'"
    )

    def __str__(self):
        return f"Order #{self.id} - {self.status}"
