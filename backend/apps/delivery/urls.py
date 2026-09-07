from django.urls import path

from . import views

urlpatterns = [
    path(
        "delivery/profile/",
        views.DeliveryPartnerProfileView.as_view(),
        name="delivery-profile",
    ),
    path(
        "delivery/assign/",
        views.AssignOrderView.as_view(),
        name="delivery-assign",
    ),
    path(
        "delivery/assignments/<int:pk>/",
        views.DeliveryAssignmentDetailView.as_view(),
        name="delivery-assignment-detail",
    ),
]