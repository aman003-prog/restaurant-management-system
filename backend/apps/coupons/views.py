from django.shortcuts import render
from django.utils import timezone
from rest_framework import generics, status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.core.permissions import IsManager
from apps.cart.models import Cart
from .models import Coupon
from .serializers import CouponSerializer, ApplyCouponSerializer

# Create your views here.
class CouponListCreateView(generics.ListCreateAPIView):
    serializer_class = CouponSerializer

    def get_permissions(self):
        # Managers can create coupons; authenticated users can list active coupons
        if self.request.method == "POST":
            return [IsAuthenticated(), IsManager()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name="Manager").exists():
            return Coupon.objects.all()
        
        now = timezone.now()
        return Coupon.objects.filter(is_active=True, valid_from__lte=now, valid_until__gte=now)


class SingleCouponView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated, IsManager]
    queryset = Coupon.objects.all()


class CouponApplyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ApplyCouponSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data["code"].strip().upper()

        # 1. Check if coupon exists
        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoesNotExist:
            return Response(
                {"detail": "Invalid coupon code."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # 2. Check if coupon is currently active & valid
        if not coupon.is_valid:
            return Response(
                {"detail": "This coupon has expired or is inactive."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 3. Fetch user's cart subtotal
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response(
                {"detail": "Your cart is empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart_total = sum(item.price for item in cart_items)

        # 4. Validate minimum order amount
        if cart_total < coupon.min_order_amount:
            return Response(
                {
                    "detail": f"Minimum order amount of {coupon.min_order_amount} required for this coupon."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 5. Calculate discount amount
        discount_amount = coupon.calculate_discount(cart_total)
        final_total = max(cart_total - discount_amount, 0)

        return Response(
            {
                "coupon_code": coupon.code,
                "cart_total": cart_total,
                "discount_amount": discount_amount,
                "final_total": final_total,
            },
            status=status.HTTP_200_OK,
        )