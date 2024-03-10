import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeService:
    @staticmethod
    def create_stripe_product(name, description=None):
        product = stripe.Product.create(
            name=name,
            description=description,
        )
        return product

    @staticmethod
    def create_stripe_price(product_id, unit_amount, currency='usd'):
        price = stripe.Price.create(
            product=product_id,
            unit_amount=unit_amount,
            currency=currency,
        )
        return price

    @staticmethod
    def create_stripe_session(price_id, success_url, cancel_url):
        success_url = 'http://example.com/success'
        cancel_url = 'http://example.com/cancel'
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return session

    @staticmethod
    def retrieve_stripe_session(session_id):
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            return session
        except stripe.error.StripeError as e:
            print(e)
            return None
