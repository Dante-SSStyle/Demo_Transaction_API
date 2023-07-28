from rest_framework import serializers
from Client.models import ExtendedUser


class TransactionForm(serializers.Serializer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fields["users"].choices = ExtendedUser.objects.all()

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


