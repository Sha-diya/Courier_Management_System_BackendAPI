from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from decimal import Decimal

from .models import User, Order


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)  # confirm password

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'role')
        extra_kwargs = {
            'role': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role')


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    delivery_man = serializers.StringRelatedField(read_only=True)

    delivery_man_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role=User.Roles.DELIVERY_MAN),
        source='delivery_man',
        write_only=True,
        required=False,
        allow_null=True,
    )

    total_amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True
    )

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'delivery_man',
            'delivery_man_id',
            'pickup_address',
            'delivery_address',
            'package_details',
            'total_amount',
            'status',
            'is_paid',
            'payment_method',
            'stripe_payment_intent',
        ]
        read_only_fields = [
            'id',
            'user',
            'status',
            'is_paid',
            'payment_method',
            'stripe_payment_intent',
        ]

    def validate_total_amount(self, value):
        if value is None:
            raise serializers.ValidationError("Total amount is required.")
        if value <= Decimal('0.00'):
            raise serializers.ValidationError("Total amount must be greater than 0.")
        return value


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # This returns a uniform success structure for login as you want
        return {
            
                "access": data.get("access"),
                "refresh": data.get("refresh"),
                "user": {
                    "id": self.user.id,
                    "username": self.user.username,
                    "email": self.user.email,
                    "role": self.user.role
                }
            
        }
