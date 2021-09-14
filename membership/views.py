from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import stripe

YOUR_DOMAIN = "http://localhost:8000"

stripe.api_key = "sk_test_"


def index(request):
    return render(request, "membership/index.html")


def create_checkout_session(request):
    if request.method == "POST":
        try:
            prices = stripe.Price.list(
                lookup_keys=[].append(request.POST["lookup_key"]),
                expand=["data.product"],
            )
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price": prices.data[0].id,
                        "quantity": 1,
                    },
                ],
                mode="subscription",
                success_url=YOUR_DOMAIN + "/success/session_id={CHECKOUT_SESSION_ID}",
                cancel_url=YOUR_DOMAIN + "/cancel-membership/",
            )
            return redirect(checkout_session.url)
        except Exception as e:
            print(e)
            return "Server error", 500


def checkout_success(request, id):
    return render(request, "membership/success.html", {id: id})


def checkout_cancel(request):
    return render(request, "membership/cancel.html")

endpoint_secret = "whsec_"

@csrf_exempt
def webhook(request):
    event = None
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        raise e
    except stripe.error.SignatureVerificationError as e:
        raise e

    # Handle the event
    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        print(payment_intent)
    else:
        print("Unhandled event type {}".format(event["type"]))

    return HttpResponse(status=200)
