from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.

class HomeView(TemplateView):
    template_name = "index1.html"

    def get(self, request):
        try:
            return render(request, 'index.html')
        except Exception as error:
            return render(request, '404.html')
