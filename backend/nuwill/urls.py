from django.urls import path
from .views import IndexView, AddKinView, GrantView, \
    AddKeyView, DecryptView

urlpatterns = [
    path('add-key/', AddKeyView.as_view(), name='add_key'),
    path('add-kin', AddKinView.as_view(), name='add_kin'),
    path('grant-kin', GrantView.as_view(), name='grant_kin'),
    path('decrypt-key', DecryptView.as_view(), name='decrypt_key'),
]
