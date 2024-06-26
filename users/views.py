from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Payment, User
from materials.serializers import PaymentSerializer

from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer
from .services import create_stripe_price, create_stripe_session


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ["paid_course", "paid_lesson", "payment_method"]
    ordering_fields = ["payment_date"]
    ordering = ["payment_date"]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product_name = "Unknown Product"
        if payment.paid_course:
            product_name = payment.paid_course
        elif payment.paid_lesson:
            product_name = payment.paid_lesson

        price = create_stripe_price(payment.amount, product_name)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
