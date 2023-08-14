from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from Client.models import ExtendedUser


class TransactionForm(serializers.Serializer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fields["users"].choices = ExtendedUser.objects.all()
        self.users_errors = []
        self.numbers_errors = []
        self.summ_errors = []
        self.recipient_list = ExtendedUser.objects.none()

    users = serializers.ChoiceField(
        choices=[],
        label="Отправитель"
    )
    numbers = serializers.CharField(
        min_length=1,
        max_length=150,
        style={'placeholder': "Введите ИНН получателей через запятую"},
        label="Получатели"
    )
    summ = serializers.DecimalField(
        min_value=1.00,
        decimal_places=2,
        max_digits=10,
        style={'placeholder': 100.00, 'input_type': 'float'},
        label="Сумма перевода"
    )

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def validate_users(self, user: str) -> str:
        form_data = self.get_initial()
        summ = float(form_data["summ"])
        numbers = form_data["numbers"].split(",")

        # Проверка на наличие ИНН у отправителя
        if not user.ITN:
            self.users_errors.append(f"Не найден ИНН для пользователя {user.username}.")

        # Проверка баланса пользователя
        if user.balance < summ:
            self.summ_errors.append(f"На счету пользователя {user.username} недостаточно средств.")

        # Проверка, что отправитель не указал свой же ИНН для перевода
        for number in numbers:
            number = number.strip()

            if number == user.ITN:
                self.numbers_errors.append(f"{number}: В списке получателей найден ИНН отправителя {user.username}.")

        if self.users_errors:
            raise ValidationError(self.users_errors)

        return user

    def validate_numbers(self, numbers: str) -> str:
        numbers_list = numbers.split(",")

        for number in numbers_list:
            number = number.strip()

            # Валидация ИНН
            if not number.isnumeric():
                error = "ИНН не может содержать буквы."
                self.numbers_errors.append(error) if error not in self.numbers_errors else error
            if len(number) == 10 or len(number) == 12:
                pass
            else:
                error = "Длина ИНН должна быть 10 или 12 цифр."
                self.numbers_errors.append(error) if error not in self.numbers_errors else error

            # Проверка, что пользователь с указанным ИНН существует
            # Использую .filter, а не .get, чтобы получить query для массового обновления получателей в дальнейшем
            recipient = ExtendedUser.objects.filter(ITN=number)
            if not recipient:
                error = f"Пользователь с ИНН {number} не существует."
                self.numbers_errors.append(error) if len(number) == 10 or len(number) == 12 else error

            # Конкатенация query с получателями
            self.recipient_list = self.recipient_list | recipient

        if self.numbers_errors:
            raise ValidationError(self.numbers_errors)

        return numbers_list

    def validate_summ(self, value: str) -> str:
        if self.summ_errors:
            raise ValidationError(self.summ_errors)
        return value



