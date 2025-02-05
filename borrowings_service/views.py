from datetime import timezone

from django.conf import settings
from django.http import JsonResponse

from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from rest_framework import viewsets, permissions
import stripe
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.generics import get_object_or_404

from borrowings_service.models import Borrowing, Payment
from borrowings_service.permissions import IsAdminAllORIsAuthenticatedReadOnly
from borrowings_service.serializers import BorrowingSerializer, BorrowingListSerializer, PaymentSerializer

from borrowings_service.tasks import notify_new_borrowing, notify_successful_payment


class BorrowingsViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all().select_related()
    serializer_class = BorrowingSerializer
    permission_classes = [IsAdminAllORIsAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowingSerializer
        elif self.action == "list":
            return BorrowingListSerializer
        else:
            return BorrowingSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == 'list':
            return queryset.select_related('user_id', 'book_id')
        return queryset

    def perform_create(self, serializer):
        borrowing = serializer.save(user_id=self.request.user)
        payment = Payment.objects.create(
            borrowing_id=borrowing,
            money_to_pay=borrowing.total_price)
        create_checkout_session(payment)
        # notify_new_borrowing(borrowing.id)
        notify_new_borrowing.delay(borrowing.id)


    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='is_active',
                type=str,
                description='Active borrowings its borrowings where return day is None',
                required=False,
                examples=[
                    OpenApiExample(
                        'Example 1',
                        description="Find route with destination 'Gare do Oriente'",
                        value=True
                    ),
                ],
            ),
            OpenApiParameter(
                name='user_id',
                type=str,
                description="Find borrowings by specific user. Only for administrators",
                required=False,
                examples=[
                    OpenApiExample(
                        'Example 1',
                        description="Find borrowings by specific user",
                        value=1
                    ),
                ],
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]


class SuccessView(View):
    def get(self, request, *args, **kwargs):
        payment_id = request.GET.get('payment_id')
        payment = get_object_or_404(Payment, id=payment_id)

        payment.status = "PAID"
        payment.save()
        return JsonResponse({"message": "Payment successful!"})


class CancelView(View):
    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        payment = get_object_or_404(Payment, session_id=session_id)
        payment.status = "PENDING"
        payment.save()
        borrowing = payment.borrowing_id

        return JsonResponse({"message": "Payment cancelled or paused."})



def create_checkout_session(payment: Payment) -> str:
    stripe.api_key = settings.STRIPE_SECRET_KEY

    if not stripe.api_key:
        raise ValueError(
            "Stripe secret key " "is not set in environment variables"
        )

    try:
        borrowing = Borrowing.objects.get(payments=payment)
        line_items = []
        product = stripe.Product.create(
            name=borrowing.book_id.title,
        )
        price = stripe.Price.create(
            unit_amount=int(borrowing.total_price * 100),
            currency="usd",
            product=product.id,
        )

        line_items.append(
            {
                "price": price.id,
                "quantity": 1,
            }
        )

        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode="payment",
            success_url=f"{settings.DOMAIN_NAME}/success?payment_id={payment.id}",
            cancel_url=f"{settings.DOMAIN_NAME}/cancel?session_id={payment.session_id}",
            metadata={
                "order_id": payment.id,
            },
        )
        payment.session_url = checkout_session.url
        payment.save()
        return checkout_session.url
    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


@csrf_exempt
def my_webhook_view(request):

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
        )
    except ValueError as e:
    # Invalid payload
        print('Error parsing payload: {}'.format(str(e)))
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
    # Invalid signature
        print('Error verifying webhook signature: {}'.format(str(e)))
        return HttpResponse(status=400)
        # Handle the event

    if event["type"] == "checkout.session.completed":
        try:
            payment_pk = event["data"]["object"]["metadata"]["payment_pk"]
            print(payment_pk)
            notify_successful_payment.delay(payment_pk)
        except Exception:
            return HttpResponse(status=500)
    return HttpResponse(status=200)
