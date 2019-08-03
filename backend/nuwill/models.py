from django.db import models

class UserSecret(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    policy_encrypting_key = models.CharField("Alice policy Privacy encryption key", 
                                             max_length=100)
    label = models.CharField("Policy Label to identify", max_length=10)
    # Tobe removed in the next release and use IPFS
    message_kit = models.TextField("MessageKit")

    class Meta:
        verbose_name = "User secret"
        verbose_name_plural = "Users secret"


class UserNextKin(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    bob_email_address = models.EmailField("Bob Email Address", editable=False)
    bob_public_address = models.CharField("Bob Public Address", 
                                          editable=False, 
                                          max_length=40)
    ipfs_address = models.TextField("IPFS Hash")

    class Meta:
        verbose_name = "User's next of kin"
        verbose_name_plural = "User's next of kin"
