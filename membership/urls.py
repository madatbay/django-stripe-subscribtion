from django.urls import path
from .views import checkout_cancel, checkout_success, index, create_checkout_session, webhook

app_name = "membership"

urlpatterns = [
    path("", index, name="index"),
    path("create-checkout-session/", create_checkout_session, name="create-checkout-session"),
    path("success/session_id=<id>/", checkout_success, name="checkout-success"),
    path("cancel-membership/", checkout_cancel, name="checkout-cancel"),
    path("membership-webhook/", webhook, name="membership-webhook"),
]
