from django.db import models

# Create your models here.

class UserSecret(models.Model):
    alice_public_key = models.CharField("Alice Public Key", max_length=40, 
                                        editable=False)
    bob_public_key = models.CharField("Bob Public Key", max_length=40, 
                                        editable=False)
    alice_private_key = models.CharField("Alice Private Key", max_length=40, 
                                        editable=False)
    bob_private_key = models.CharField("Bob Private Key", max_length=40, 
                                        editable=False)

    class Meta:
        verbose_name = "User secret"
        verbose_name_plural = "Users secret"


class UserNextKin(models.Model):
    bob_email_address = models.EmailField("Bob Email Address", editable=False)
    bob_public_address = models.CharField("Bob Public Address", 
                                          editable=False, 
                                          max_length=40)
    ipfs_address = models.TextField("IPFS Hash")

    class Meta:
        verbose_name = "User's next of kin"
        verbose_name_plural = "User's next of kin"
