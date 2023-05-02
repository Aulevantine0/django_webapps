from django import forms


# class LoginForm(forms.Form):
#     username = forms.CharField(required=True, widget=forms.TextInput(attrs={}))
#     password = forms.CharField(required=True, widget=forms.TextInput(attrs={"type": "password"}))
#
#     class Meta:
#         fields = ["username", "password"]


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class RegisterForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "form-control"
            }
        ))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last Name",
                "class": "form-control"
            }
        ))
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    currency = forms.ChoiceField(
        choices=[(1, 'USD'), (2, 'GBP'), (3, 'EURO')],
        widget=forms.Select(
            attrs={
                "placeholder": "",
                "class": "form-control"
            }
        ))
