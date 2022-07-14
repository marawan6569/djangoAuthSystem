from django.core.exceptions import ValidationError


def validate_phone_length(phone: str):
    if len(phone) <= 10:
        raise ValidationError(message="phone number is too short.")

    if len(phone) >= 15:
        raise ValidationError(message="phone number is too long.")


def validate_phone_starts_with_plus(phone: str):
    if not phone.startswith('+'):
        raise ValidationError(message="phone number must start with '+'.")


def validate_phone_is_num(phone: str):
    if not phone[1:].isnumeric():
        raise ValidationError(message="phone number must be only numbers.")


phone_number_validation = [validate_phone_length, validate_phone_starts_with_plus, validate_phone_is_num]
