from django.views.generic import FormView
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .models import User
from .forms import SignupForm, LoginForm


class SignupAsStudent(FormView):
    form_class = SignupForm
    template_name = 'authentication/signup/signup.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.is_student = True
        form.save()
        return super().form_valid(form)


class SignupAsTeacher(FormView):
    form_class = SignupForm
    template_name = 'authentication/signup/signup.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.is_teacher = True
        form.save()
        return super().form_valid(form)


class Login(FormView):
    form_class = LoginForm
    template_name = 'authentication/login/login.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            login_with = form.cleaned_data['login_with']
            password = form.cleaned_data['password']
            if login_with == 'phone':
                phone = form.cleaned_data['phone_or_email']
                user = authenticate(phone_number=phone, password=password)
            elif login_with == 'email':
                email = form.cleaned_data['phone_or_email']
                user = authenticate(phone_number=User.objects.get(email=email).phone_number, password=password)
                print(user)
            else:
                raise ValidationError('wrong Email/phone or password')
            if user:
                login(self.request, user)
                return JsonResponse({})
            else:
                raise ValidationError('wrong Email/phone or password')
        else:
            raise ValidationError('wrong Email/phone or password')