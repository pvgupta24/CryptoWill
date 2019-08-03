from django.shortcuts import render
from django.views import View


class IndexView(View):

    def get(self, request):
        template_name = "index.html"
        return render(request, template_name)

