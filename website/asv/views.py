import json
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

        trucks = list(Truck.objects.filter(**params).values())
        return JsonResponse({ 'data': trucks })
    
class Upload(BaseView):
    template_name = 'asv/upload.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        file = request.FILES["upload_file"]

        if not ".csv" not in file:
            return HttpResponseBadRequest("CSV Only.")

        trucks_to_create = []
        data = handle_uploaded_file(file)

        for row in data:
            sale_date = ""
            if not '\ufeffSale_Date' in row:
                sale_date = row.get('Sale_Date')
            else:
                sale_date = row.get('\ufeffSale_Date')

            truck = Truck(
            sale_date=sale_date,
            vin=row.get('VIN'),
            saledocumenttype=row.get('SaleDocumentType'),
            loss_type=row.get('Loss_Type'),
            damage_description_primary=row.get('Damage_Description_Primary'),
            starts_at_checkin=row.get('Starts_At_CheckIn'),
            runs_and_drives=row.get('Runs_And_Drives'),
            miles=row.get('Miles'),
            offer=row.get('Offer'),
            odometerreadingtypedescription=row.get('OdometerReadingTypeDescription'),
            air_bags_deployed=row.get('Air_Bags_Deployed'),
            saleprice=row.get('SalePrice'),
            branch=row.get('Branch'),
            branch_zip_code=row.get('Branch_Zip_Code'),
            drivelinetype=row.get('DriveLineType'),
            year=row.get('Year'),
            make=row.get('Make'),
            model=row.get('Model'),
            trim=row.get('Trim'),
            bodytype=row.get('BodyType'),
            cabtype=row.get('CabType'),
            fueltype=row.get('FuelType'),
            enginesize=row.get('EngineSize'),
            data_type=row.get('Data_Type'),
            stateabbreviation=row.get('StateAbbreviation')
            )

            trucks_to_create.append(truck)

        Truck.objects.bulk_create(trucks_to_create)
        return render(request, self.template_name)