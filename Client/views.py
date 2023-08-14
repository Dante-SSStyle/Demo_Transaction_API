from django.db import transaction, IntegrityError
from django.db.models import F
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from Client.forms import TransactionForm


class Transactions(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "transaction.html"

    def get(self, request: Request) -> Response:
        serializer = TransactionForm()
        return Response({"form": serializer})

    def post(self, request: Request) -> Response:
        serializer = TransactionForm(data=request.data)

        if serializer.is_valid():
            user = serializer['users'].value
            summ = float(serializer['summ'].value)
            summ_part = summ / len(serializer.recipient_list)

            # Обновление отправителя и получателей
            try:
                with transaction.atomic():
                    user.balance = float(user.balance) - summ
                    user.save()
                    serializer.recipient_list.update(balance=F('balance') + summ_part)
            except IntegrityError:
                return Response(
                    {"form": serializer, "error": "Ошибка базы данных.", "color": "red"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response({"form": TransactionForm(), "error": "Успешная транзакция", "color": "black"})
        else:
            return Response(
                {"form": serializer, "error": "Ошибка ввода данных.", "color": "red"},
                status=status.HTTP_400_BAD_REQUEST
            )
