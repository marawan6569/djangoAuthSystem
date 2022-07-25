from django.core.exceptions import ValidationError
import string
from os.path import splitext


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


def validate_image_extension(value):
    allowed_extension = ['.png', '.jpg', '.jpeg']
    if splitext(value.name)[1].lower() not in allowed_extension:
        raise ValidationError('Unsupported file type.')


def validate_password_length(value):
    if len(value) < 8:
        raise ValidationError('Password must be at lest 8 character')


def validate_password(value):
    is_cap = False
    is_small = False
    is_digit = False
    is_special = False
    for char in value:
        if char in string.ascii_uppercase:
            is_cap = True
            continue

        if char in string.ascii_lowercase:
            is_small = True
            continue

        if char in string.digits:
            is_digit = True
            continue

        if char in string.punctuation:
            is_special = True

    if not (is_cap and is_small and is_digit and is_special):
        raise ValidationError('Password must contains at lest one '
                              '(capital character, small character, digit, special character)')


phone_number_validation = [validate_phone_length, validate_phone_starts_with_plus, validate_phone_is_num]
password_validators = [validate_password_length, validate_password]
