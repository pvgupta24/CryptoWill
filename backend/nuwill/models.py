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
