from django import forms


class SecretForm(forms.Form):
    alice_private_key = forms.CharField("Enter your private key")
