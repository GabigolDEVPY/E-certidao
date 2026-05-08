from django.views import View
from django.shortcuts import render, redirect
from .forms import OrderImovelForm


class ImovelView(View):
    template_name = 'certidao_imovel.html'

    def get(self, request):
        form = OrderImovelForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = OrderImovelForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.usuario = request.user
            order.save()
            
            return redirect('/pagamento/')
        return render(request, self.template_name, {'form': form})
