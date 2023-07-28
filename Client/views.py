from django.core.exceptions import ValidationError
from django.db.models import F
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from Client.forms import TransactionForm
from Client.models import ExtendedUser
from Client.validators import validate_itn


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
            numbers = [number.strip() for number in serializer['numbers'].value.split(",")]
            summ = float(serializer['summ'].value)

            # Проверка на наличие ИНН у отправителя
            if not user.ITN:
                return Response(
                    {"form": serializer, "error": f"Не найден ИНН для пользователя {user.username}.", "color": "red"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Проверка баланса пользователя
            if user.balance < summ:
                return Response(
                    {"form": serializer, "error": f"На счету пользователя {user.username} недостаточно средств.", "color": "red"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Создание пустого query для массового обновления получателей в дальнейшем
            recipient_list = ExtendedUser.objects.none()

            for number in numbers:
                # Валидация ИНН
                try:
                    validate_itn(number)
                except ValidationError as err:
                    return Response(
                        {"form": serializer, "error": f"{number}: {err.message}", "color": "red"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                # Проверка, что отправитель не указал свой же ИНН для перевода
                if number == user.ITN:
                    return Response(
                        {"form": serializer, "error": f"{number}: В списке получателей найден ИНН отправителя {user.username}.", "color": "red"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                # Проверка, что пользователь с указанным ИНН существует
                # Использую .filter, а не .get, чтобы получить query для массового обновления получателей в дальнейшем
                recipient = ExtendedUser.objects.filter(ITN=number)
                if not recipient:
                    return Response(
                        {"form": serializer, "error": f"Пользователь с ИНН {number} не существует.", "color": "red"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
                # Конкатенация query с получателями
                recipient_list = recipient_list | recipient

            summ_part = summ / len(recipient_list)

            # Обновление отправителя и получателей
            user.balance = float(user.balance) - summ
            user.save()
            recipient_list.update(balance=F('balance') + summ_part)

            return Response({"form": TransactionForm(), "error": "Успешная транзакция", "color": "black"})
        else:
            return Response(
                {"form": serializer, "error": "Ошибка ввода данных.", "color": "red"},
                status=status.HTTP_400_BAD_REQUEST
            )
