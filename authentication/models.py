from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.utils.timezone import make_aware
from django.db import models

from datetime import datetime, timedelta
from random import randint
from string import ascii_letters, digits

from .managers import UserManager, StudentManager, TeacherManager
from .validations import phone_number_validation, password_validators, validate_image_extension


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(
                                    max_length=14, unique=True, verbose_name='phone number',
                                    validators=phone_number_validation,
                                    help_text='Must be in E.164 format i.e. +xxxxxxxxxxx .'
                                    )
    email = models.EmailField(unique=True, verbose_name='email address')
    first_name = models.CharField(max_length=30, blank=True, verbose_name='first name')
    last_name = models.CharField(max_length=30, blank=True, verbose_name='last name')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='date joined')
    avatar = models.ImageField(
                                upload_to='avatars/', null=True, blank=True,
                                validators=[validate_image_extension],
                                help_text='Supported content types: jpg, jpeg, png .'
                               )

    password = models.CharField(
                                max_length=128,
                                verbose_name="password",
                                help_text='Password must contains at lest one '
                                          '(capital character, small character, digit, special character)'
                                          ' and must be at lest 8 characters',
                                validators=password_validators)

    is_active = models.BooleanField(default=False, verbose_name='active')
    is_staff = models.BooleanField(default=False, verbose_name='staff')
    is_student = models.BooleanField(default=False, verbose_name='student')
    is_teacher = models.BooleanField(default=False, verbose_name='teacher')

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()
    students = StudentManager()
    teachers = TeacherManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def activate(self):
        self.is_active = True
        self.save()

    def deactivate(self):
        self.is_active = False
        self.save()

    def send_confirmation_code(self):
        old_codes = ConfirmationCodes.objects.filter(user=self).first()
        if old_codes:
            pass
        else:
            code = ConfirmationCodes.objects.create(user=self)

    def confirm(self, entered_code):
        code = ConfirmationCodes.objects.filter(user=self).first()
        if not code:
            return False
        else:
            if code.valid_until > make_aware(datetime.now()):
                if entered_code == code.code:
                    self.activate()
                    code.delete()
                    return True
                else:
                    return False
            else:
                return False

    def __str__(self):
        return self.get_full_name() or self.phone_number


class ConfirmationCodes(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='confirmation_code')
    code = models.CharField(max_length=9, editable=False)
    valid_until = models.DateTimeField(default=make_aware(datetime.now() + timedelta(minutes=5)))

    @staticmethod
    def _generate_code():
        letter_and_digits = ascii_letters + digits
        code = ''
        for idx in range(9):
            code += letter_and_digits[randint(0, len(letter_and_digits) - 1)]

        return code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self._generate_code()
        return super(ConfirmationCodes, self).save(*args, **kwargs)

    def __str__(self):
        return self.code
