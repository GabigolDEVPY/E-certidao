from django.contrib import admin
from django.urls import path
from . views import HomeView, PrivacyPolicyView, TermsOfUseView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('privacidade/', PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('termos/', TermsOfUseView.as_view(), name='terms_of_use'),
]
