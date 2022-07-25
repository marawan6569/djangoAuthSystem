from django.urls import path
from .views import SignupAsStudent, SignupAsTeacher, Login, ConfirmView

app_name = 'authentication'


urlpatterns = [
    path('signup/student', SignupAsStudent.as_view(), name='signup_as_student'),
    path('signup/teacher', SignupAsTeacher.as_view(), name='signup_as_teacher'),
    path('login/', Login.as_view(), name='login'),
    path('confirm/', ConfirmView.as_view(), name='confirm'),
]
