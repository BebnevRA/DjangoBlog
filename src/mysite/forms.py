from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django import forms


class RegisterForm(UserCreationForm):
    GROUP_CHOICES = Group.objects.filter(Q(name='Author') | Q(name='Subscriber'))
    email = forms.EmailField(label="Email")
    group = forms.ModelChoiceField(queryset=GROUP_CHOICES, empty_label=None)

    class Meta:
        model = User
        fields = ("email", "group")

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password2'].help_text = None
        self.fields['password1'].help_text = None

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.username = user.email
        if commit:
            user.save()
        group = Group.objects.get(name=self.cleaned_data["group"])
        user.groups.add(group)
        return user

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email already used")
        return data




