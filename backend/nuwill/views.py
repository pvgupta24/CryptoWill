import requests

from django.shortcuts import render
from django.views import View
from django.core.mail import send_mail
from django.conf import settings

from .forms import SecretForm, UserNextKinForm
from .models import UserSecret, UserNextKin
from .utils import generate_word

class IndexView(View):
    """
    Landing page for Alice and login with Django Admin
    """
    def get(self, request):
        template_name = "index.html"
        return render(request, template_name)


class AboutView(View):
    """
    About CryptoWill page
    """
    def get(self, request):
        template_name = "about.html"
        return render(request, template_name)


class ContactView(View):
    """
    Contact CryptoWill team to signup on platform
    """
    def get(self, request):
        template_name = "contact.html"
        return render(request, template_name)


class AddKeyView(View):
    """
    Alice secures private key.
    Key is encrypted immediately and stored to database
    """
    def get(self, request):
        form = SecretForm()
        template_name = "add-key.html"
        context = {
            'form': form
        }
        return render(request, template_name, context)

    def post(self, request):
        template_name = "add-key.html"
        form = SecretForm(request.POST)
        if form.is_valid():
            template_name = "add-kin.html"

            private_key = form.data['alice_private_key']

            # Generate Policy and Store policy_encryption_key to db UserSecret as well
            label = generate_word(5)
            res = requests.post('http://127.0.0.1:8151/derive_policy_encrypting_key/'+label)
            data = res.json()

            policy_encrypting_key = data['result'].get('policy_encrypting_key')

            # alice's private key encrypted with nucypher, Not saving to db
            # Enrico encryption here. Great work Enrico.
            payload = {
                'message': private_key
            }
            res1 = requests.post('http://127.0.0.1:5000/encrypt_message', json=payload)

            data = res1.json()

            message_kit = data['result'].get('message_kit')

            # Store MessageKit and label into UserSecret model
            UserSecret.objects.create(
                user=request.user,
                label=label,
                policy_encrypting_key=policy_encrypting_key,
                message_kit=message_kit
            )

            form = UserNextKinForm()
            context = {
                'form': form,
                'alice_encrypted_key': message_kit
            }
            return render(request, template_name, context)
        return render(request, template_name, form=form)


class AddKinView(View):
    """
    Alice submit's next of keen's email and public-key GET page
    """
    def post(self, request):
        # Not doing anything with Nucypher here. Just store and move.
        template_name = 'add-kin.html'
        form = UserNextKinForm(request.POST)
        if form.is_valid():
            template_name = 'index.html'
            form.save()  # save bob's details to db for given user
            context = {
                'message': "Congratulations! We have added your kin's details. \
                            Now we'll send you periodically email. Make sure \
                            to click on the link provided in the email to \
                            avoid granting access to your kin. If you fail so \
                            clicking on the link, we'll grant access to your \
                            kin and you kin will able to decrypt the message."
            }
            return render(request, template_name, context)

        context = {
            "form": form
        }
        return render(request, template_name, context)


class GrantView(View):
    """
    Alice failed to confirm email link and thus delegation takes place
    Called internally by the triggers
    """
    # adding bob into the alice's policy and re-encrypting the hash, so that
    # bob can decrypt it later.
    # send mail to bob with the link to access hash IPFS data

    def get(self, request):
        template_name = "grant.html"
        return render(request, template_name)

    def post(self, request):
        template_name = "grant.html"
        # ToDo: Get label for this user
        label = ''
        payload = {
            "bob_encrypting_key": settings.BOB_ENCRYPTING_KEY,
            "label": label,
            "m": 1,
            "n": 1,
            "expiration" : "2020-11-11T11:11:11",
            "bob_verifying_key": settings.BOB_VERIFYING_KEY
        }
        res1 = requests.post('http://localhost:8151/grant', data=payload)
        data = res1.json()
        # ToDo: Store this keys in the DB and will be used to decrypt the message
        policy_encrypting_key = data['policy_encrypting_key']
        alice_verifying_key = data['alice_verifying_key']
        return render(request, template_name)


class DecryptView(View):
    """
    Bob submits Alice's IPFS payload and we decrypt it for him.
    Only once! It can be requested only once and also decrypted only once.
    """
    def get(self, request):
        template_name = "decrypt-key.html"
        return render(request, template_name)

    def post(self, request):
        template_name = "decrypt-key.html"
        # ToDo: get the hash file and decrypt it with Nucypher.
        # Send secret back to Bob without storing it anywhere
        policy_encrypting_key = ''
        alice_verifying_key = ''
        label = ''
        message_kit = ''

        payload = {
            "policy_encrypting_key": policy_encrypting_key,
            "alice_verifying_key": alice_verifying_key,
            "label": label,
            "message_kit": message_kit
        }
        res1 = requests.post('localhost:4000/retrieve', data=payload)
        data = res1.content
        # We are only passing one message while encryping.
        # Get the first one only.
        decrypted_message = data.result.get('cleartexts')[0]
        context = {
            'decrypted_message': decrypted_message
        }
        return render(request, template_name, context)


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
