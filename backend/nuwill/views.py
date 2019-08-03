from django.shortcuts import render
from django.views import View


class IndexView(View):
    """
    Landing page for Alice and login with Torus
    """

    def get(self, request):
        template_name = "index.html"
        return render(request, template_name)


class SignupView(View):
    """
    Alice secures private key.
    Key is encrypted immediately and stored to database
    """
    pass


class RollView(View):
    """
    Alice submit's next of keen's email and public-key GET page
    """
    pass


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
