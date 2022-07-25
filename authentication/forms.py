import re
from django.forms import Form, ModelForm, CharField,TextInput, PasswordInput, ValidationError
from .models import User


class SignupForm(ModelForm):
    password = CharField(
        widget=PasswordInput(),
        help_text='Password must contains at lest one '
                  '(capital character, small character, digit, special character) and must be at lest 8 characters'
    )

    password2 = CharField(
        label="Password confirmation",
        widget=PasswordInput(),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password and password2:
            if password != password2:
                raise ValidationError("Passwords didn't match.")
            else:
                return password2

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password', 'password2', 'avatar']


class LoginForm(Form):

    @staticmethod
    def _is_valid_email(email: str):
        regex = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}'
        return True if re.fullmatch(regex, email) else False

    @staticmethod
    def _is_valid_phone(phone: str):
        status = 0
        if 15 > len(phone) > 10:
            status += 1
        if phone.startswith('+'):
            status += 1
        if phone[1:].isnumeric():
            status += 1

        return True if status == 3 else False

    phone_or_email = CharField(
        max_length=128,
        widget=TextInput(attrs={'placeholder': 'please enter your email or phone number.'})
    )

    password = CharField(
        max_length=128,
        widget=PasswordInput(attrs={'placeholder': 'please enter your password.'})
    )

    def clean_phone_or_email(self):
        status = 0
        email_or_phone = self.cleaned_data['phone_or_email']
        if self._is_valid_email(email_or_phone):
            self.cleaned_data['login_with'] = 'email'
            status += 1
        if self._is_valid_phone(email_or_phone):
            self.cleaned_data['login_with'] = 'phone'
            status += 1

        if status == 0:
            raise ValidationError('Not valid email or phone number')
        else:
            return email_or_phone
