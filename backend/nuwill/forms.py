from django import forms


class SecretForm(forms.Form):
    alice_private_key = forms.CharField(label="Enter your private key", 
                                        max_length=40)
    


class UserNextKinForm(forms.Form):
    bob_email_address = forms.EmailField(label="Bob's Email address")
    bob_public_address = forms.CharField(label="Bob's Public address", 
                                         max_length=40)
    ipfs_hash = forms.CharField(label='IPFS hash of the payload', 
                                max_length=300, required=False)
