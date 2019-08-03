from django.urls import path
from .views import IndexView, SignupView, RollView, DelegateView, \
    DecryptView

urlpatterns = [
    path('submit/', SignupView.as_view(), name='signup'),
    path('roll', RollView.as_view(), name='roll'),
    path('delegate', DelegateView.as_view(), name='delegate'),
    path('decrypt', DecryptView.as_view(), name='decrypt'),
    # path('api/v1/store', StoreView.as_view(), name='store'),
]
