from django.core.exceptions import ValidationError


def validate_itn(value: str) -> str:
    if not value.isnumeric():
        raise ValidationError("ИНН не может содержать буквы.")
    if len(value) == 10 or len(value) == 12:
        return value
    else:
        raise ValidationError("Длина ИНН должна быть 10 или 12 цифр.")
