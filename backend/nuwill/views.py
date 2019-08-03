import json
import base64

from django.shortcuts import render
from django.views import View

from umbral import pre, keys, signing, params
from umbral import  config as uconfig

from .forms import SecretForm, UserNextKinForm


class IndexView(View):
    """
    Landing page for Alice and login with Torus
    """

    def get(self, request):
        template_name = "index.html"
        return render(request, template_name)


# class SignupView(View):
#     """
#     Alice secures private key.
#     Key is encrypted immediately and stored to database
#     """
#     pass


class SignupView(View):
    """
    Alice secures private key.
    Key is encrypted immediately and stored to database
    """
    def get(self, request):
        form = SecretForm(request.form)
        template_name = "signup.html"
        return render(request, template_name, form=form)

    def post(self, request):
        template_name = "signup.html"
        form = SecretForm(request.form)
        if form.is_validate():
            template_name = "roll.html"
            # Do some Nucypher stuff and save those nucypher keys to db            
            # alice's private key encrypted with nucypher, Not saving to db
            alice_encrypted_private_key = ''
            form = UserNextKinForm(request.form)
            context = {
                'form': form,
                'alice_encrypted_key': alice_encrypted_private_key
            }
            return render(request, template_name, context)
        return render(request, template_name, form=form)


class RollView(View):
    """
    Alice submit's next of keen's email and public-key GET page
    """
    def post(self, request):
        # Not doing anything with Nucypher here. Just store and move.
        template_name = 'rolls.html'
        form = UserNextKinForm(request.form)
        if form.is_valid():
            template_name = 'index.html'
            form.save()  # save bob's details to db for given user
            return render(request, template_name)
        return render(request, template_name, form=form)


class DelegateView(View):
    """
    Alice failed to confirm email link and thus delegation takes place
    """
    pass


class DecryptView(View):
    """
    Bob submits Alice's IPFS payload and we decrypt it for him.
    Only once!
    """
    pass


class StoreView(View):
    """
    Alice submit's next of keen's email, public-key and IPFS hash GET page
    """
    pass
