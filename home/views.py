from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages

from .forms import ContactMessageForm


# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'index.html')


class PrivacyPolicyView(TemplateView):
    template_name = 'privacy_policy.html'


class TermsOfUseView(TemplateView):
    template_name = 'terms_of_use.html'


class ContactView(View):
    template_name = 'contact_us.html'

    def get(self, request):
        return render(request, self.template_name, {'form': ContactMessageForm()})

    def post(self, request):
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mensagem enviada com sucesso. Retornaremos o mais breve possivel.')
            return render(request, self.template_name, {'form': ContactMessageForm()})

        messages.error(request, 'Confira os campos destacados e tente novamente.')
        return render(request, self.template_name, {'form': form})
