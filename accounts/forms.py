from django.forms import ModelForm
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm,
    PasswordResetForm, SetPasswordForm,
    UserChangeForm, UserCreationForm
)

from .models import User

class UserInfoChangeForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'email',
            'username',
        ]

    def __init__(self, email=None, username=None, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        if email:
            self.fields['email'].widget.attrs['value'] = email
        if username:
            self.fields['username'].widget.attrs['value'] = username

    def update(self, user):
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        user.save()

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

class AdminUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'
        
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email','username','is_men','is_girl')

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix','')
        super().__init__(*args, **kwargs)