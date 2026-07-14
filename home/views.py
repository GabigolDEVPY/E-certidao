from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.conf import settings


# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'index.html')


class PrivacyPolicyView(TemplateView):
    template_name = 'privacy_policy.html'


class TermsOfUseView(TemplateView):
    template_name = 'terms_of_use.html'


class ContactView(TemplateView):
    template_name = 'contact_us.html'
