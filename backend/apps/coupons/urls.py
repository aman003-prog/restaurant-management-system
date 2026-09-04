from django.urls import path
from . import views

urlpatterns = [
    path("coupons/", views.CouponListCreateView.as_view(), name="coupon-list"),
    path("coupons/apply/", views.CouponApplyView.as_view(), name="coupon-apply"),
    path("coupons/<int:pk>/", views.SingleCouponView.as_view(), name="coupon-detail"),
]