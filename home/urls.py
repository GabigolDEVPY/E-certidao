from django.contrib import admin
from django.urls import path
from . views import (
    BlogDetailView,
    BlogListView,
    CertidaoServiceView,
    ContactView,
    FAQView,
    HomeView,
    PrivacyPolicyView,
    TermsOfUseView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('blog/', BlogListView.as_view(), name='blog_list'),
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('faq/', FAQView.as_view(), name='faq'),
    path('certidoes/<slug:slug>/', CertidaoServiceView.as_view(), name='certidao_service'),
    path('privacidade/', PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('termos/', TermsOfUseView.as_view(), name='terms_of_use'),
    path('contact/', ContactView.as_view(), name='contact'),
]
