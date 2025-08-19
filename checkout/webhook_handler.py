from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})
        
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )     

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)
    
    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        # get the PaymentIntent object from the event
        intent = event['data']['object']  

        # try to read order_number from PaymentIntent metadata
        order_number = intent.get('metadata', {}).get('order_number')  

        if not order_number:
            # If metadata missing, respond but do not crash
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | No order_number in metadata',
                status=400
            )

        # lookup the order and send confirmation email
        try:
            order = Order.objects.get(order_number=order_number)  
            self._send_confirmation_email(order)  
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | Confirmation email sent for order {order_number}',
                status=200
            )
        except Order.DoesNotExist:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | Order not found (order_number={order_number})',
                status=404
            )
    
    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)