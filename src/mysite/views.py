from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from src.mysite.forms import RegisterForm


class SignUp(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
