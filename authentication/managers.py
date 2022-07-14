from django.contrib.auth.base_user import BaseUserManager
from django.db.models import QuerySet, Manager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, password, **extra_fields):
        """
        Creates and saves a User with the given phone_number and password.
        """
        if not phone_number:
            raise ValueError('The given phone number must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_student(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_student', True)
        return self._create_user(phone_number, password, **extra_fields)

    def create_teacher(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_teacher', True)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone_number, password, **extra_fields)


class StudentQuerySet(QuerySet):

    def active(self):
        return self.filter(is_active=True)


class StudentManager(Manager):
    def get_queryset(self):
        return StudentQuerySet(self.model, using=self._db).filter(is_student=True)

    def active(self):
        self.get_queryset().active()


class TeacherQuerySet(QuerySet):

    def active(self):
        return self.filter(is_active=True)


class TeacherManager(Manager):
    def get_queryset(self):
        return TeacherQuerySet(self.model, using=self._db).filter(is_teacher=True)

    def active(self):
        self.get_queryset().active()
