import os
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseBadRequest, JsonResponse
from django.core import serializers

from asv.models import Truck
from asv.utils.upload_file import handle_uploaded_file

class BaseView(View):
    domain = str(os.environ.get('DJANGO_DOMAIN'))

    context = {
        'domain': domain,
    }

    template_name = 'asv/home.html'

    def get(self, request, *args, **kwargs):
        ctx = self.context
        ctx['path'] = request.path
        return render(request, self.template_name, context=ctx)

class HomeView(BaseView):
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
class Trucks(BaseView):
    def get(self, request, *args, **kwargs):
        params = request.GET.dict()

        print(params)

        trucks = Truck.objects.all()

        JSON = serializers.get_serializer("json")
        data = JSON()
        data.serialize(trucks)
        data = data.getvalue()
        return JsonResponse(data)
    
class Upload(BaseView):
    template_name = 'asv/upload.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        file = request.FILES["upload_file"]

        if not ".csv" in file:
            return HttpResponseBadRequest("CSV Only.")

        handle_uploaded_file(file)
        return render(request, self.template_name)