import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_price(amount):
    """Создает цену в Stripe."""
    price = stripe.Price.create(
        currency="rub",
        unit_amount=int(amount * 100),
        product_data={"name": "Payment"},
    )
    return price


def create_stripe_session(price):
    """Создает сессию оплаты в Stripe."""
    session = stripe.checkout.Session.create(
        success_url="https://example.com/success/",
        cancel_url="https://example.com/cancel/",
        payment_method_types=["card"],
        line_items=[{"price": price.id, "quantity": 1}],
        mode="payment",
    )
    return session.id, session.url
