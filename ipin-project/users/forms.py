from django import forms

from . import models as users_models


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'ID',
                'type': 'text',
            }
        ),
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'type': 'password',
            }
        )
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        try:
            user = users_models.User.objects.get(username=username)

            if user.check_password(password):
                return self.cleaned_data

            self.add_error(
                'password',
                forms.ValidationError('Password is wrong', code="invalid")
            )
        except users_models.User.DoesNotExist:
            self.add_error(
                'username',
                forms.ValidationError('User does not exist', code="invalid")
            )