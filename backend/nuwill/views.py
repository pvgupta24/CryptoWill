import json
import base64
import requests

from django.shortcuts import render
from django.views import View
from django.core.mail import send_mail

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
        form = SecretForm()
        template_name = "signup.html"
        context = {
            'form': form
        }
        return render(request, template_name, context)

    def post(self, request):
        template_name = "signup.html"
        form = SecretForm(request.POST)
        if form.is_validate():
            template_name = "roll.html"

            # generate alice's Nucypher keys as below
            # Todo: Store them to db table UserSecret with FK user
            alices_private_key = keys.UmbralPrivateKey.gen_key()
            alices_public_key = alices_private_key.get_pubkey()
            alices_signing_key = keys.UmbralPrivateKey.gen_key()
            alices_verifying_key = alices_signing_key.get_pubkey()

            # Do some Nucypher stuff and save those nucypher keys to db
            hash = form.data.alice_private_key

            # alice's private key encrypted with nucypher, Not saving to db
            # Enrico encryption here. Great work Enrico.
            alice_encrypted_private_key, capsule = pre.encrypt(alices_public_key, hash)

            # Generate Policy and Store policy_encryption_key to db UserSecret as well
            label = 'name'  # random name here generating from a-z 5-7 character

            res = requests.post('http://127.0.0.1:8151/derive_policy_encrypting_key/'+label)
            data = res.content
            policy_encrypting_key = data.result.policy_encrypting_key

            # Store capsule/MessageKit and label into UserSecret model as well
            # ToDo: here

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
    Called internally by the triggers
    """
    # adding bob into the alice's policy and re-encrypting the hash, so that
    # bob can decrypt it later.
    # send mail to bob with the link to access hash IPFS data

    def get(self, request):
        template_name = "delegate.html"
        return render(request, template_name)



class DecryptView(View):
    """
    Bob submits Alice's IPFS payload and we decrypt it for him.
    Only once! It can be requested only once and also decrypted only once.
    """
    def get(self, request):
        template_name = "decrypt_page.html"
        # get the hash file and decrypt it with Nucypher.
        # Send secret back to Bob without storing it anywhere
        return render(request, template_name)


# class StoreView(View):
#     """
#     Alice submit's next of kin's email, public-key and IPFS hash GET page
#     """
#     pass


def send_periodically_mail(alice_email):
    """
    Send periodically mail to Alice for proof of life
    """
    send_mail(
        'Please confirm your heartbeat by clicking the link in this email',
        'Some body message will come here',
        'team@cryptowill.io',  # Todo: Alice's email address here
        [alice_email],
        fail_silently=False,
    )
