from django.urls import path
from .views import IndexView, AddKinView, GrantView, \
    AddKeyView, DecryptView, AboutView, ContactView, \
    send_periodically_mail

urlpatterns = [
    path('add-key/', AddKeyView.as_view(), name='add_key'),
    path('add-kin', AddKinView.as_view(), name='add_kin'),
    path('grant-kin', GrantView.as_view(), name='grant_kin'),
    path('decrypt-key', DecryptView.as_view(), name='decrypt_key'),

    path('about', AboutView.as_view(), name='about'),
    path('contact-team', ContactView.as_view(), name='contact'),
    path('send-email', send_periodically_mail, name='send_email'),

]
