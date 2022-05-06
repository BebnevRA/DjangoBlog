from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

from mysite.forms import RegisterForm, UserEditForm


class SignUp(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def user_edit(request):
    if request.method == 'POST':
        form_password = PasswordChangeForm(request.user, request.POST)
        form_user = UserEditForm(request.POST, instance=request.user)

        if form_password.is_valid() and 'change_password' in request.POST:
            user = form_password.save()
            update_session_auth_hash(request, user)
            messages.success(request,
                             'Your password was successfully updated!')
            return redirect('user_edit')

        if form_user.is_valid() and 'edit_user' in request.POST:
            user = form_user.save()
            update_session_auth_hash(request, user)
            messages.success(request,
                             'Your user data was successfully updated!')
            return redirect('user_edit')
    else:
        form_password = PasswordChangeForm(request.user)
        form_user = UserEditForm(instance=request.user)

    return render(request, 'registration/user_edit.html',
                  {'form_password': form_password, 'form_user': form_user})

