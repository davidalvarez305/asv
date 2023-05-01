import os
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from asv.models import Truck, VehicleCondition, VehicleDetails, Make, Model, Trim, Branch, Sale
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

class HomeView(LoginRequiredMixin, BaseView):
    login_url="/login"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
class Trucks(LoginRequiredMixin, BaseView):
    login_url="/login"
    def get(self, request, *args, **kwargs):
        params = request.GET.dict()

        trucks = list(Truck.objects.filter(**params).values())
        return JsonResponse({ 'data': trucks })
    
class Upload(LoginRequiredMixin, BaseView):
    login_url="/login"
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
                vin=row.get('VIN'),
                data_type=row.get('Data_Type'),
                offer=row.get('Offer'),
                vehicle_details = VehicleDetails(
                    year=row.get('Year'),
                    make = Make(
                        row.get('Make')
                    ),
                    model = Model(
                        row.get('Model')
                    ),
                    trim = Trim(
                        row.get('Trim')
                    ),
                    bodytype=row.get('BodyType'),
                    cabtype=row.get('CabType'),
                    fueltype=row.get('FuelType'),
                    enginesize=row.get('EngineSize'),
                    odometerreadingtypedescription=row.get('OdometerReadingTypeDescription'),
                    drivelinetype=row.get('DriveLineType'),
                    vehicle_condition = VehicleCondition(
                        starts_at_checkin=row.get('Starts_At_CheckIn'),
                        runs_and_drives=row.get('Runs_And_Drives'),
                        air_bags_deployed=row.get('Air_Bags_Deployed'),
                        miles=row.get('Miles'),
                        loss_type=row.get('Loss_Type'),
                        damage_description_primary=row.get('Damage_Description_Primary'),
                    ),
                    sale = Sale(
                        sale_date=sale_date,
                        saleprice=row.get('SalePrice'),
                        saledocumenttype=row.get('SaleDocumentType'),
                        branch = Branch(
                                branch=row.get('Branch'),
                                branch_zip_code=row.get('Branch_Zip_Code'),
                                stateabbreviation=row.get('StateAbbreviation')
                            )
                    ),
                )
            )
            trucks_to_create.append(truck)

        Truck.objects.bulk_create(trucks_to_create)
        return render(request, self.template_name)
    
class Login(BaseView):
    template_name = 'asv/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        form = request.POST.dict()
        user = authenticate(request=request, username=form.get('username'), password=form.get('password'))

        if user is not None:
            login(request, user)
            return JsonResponse({ 'data': 'Success.'}, status=200)
        else:
            return JsonResponse({ 'data': 'Authentication failed.'}, status=400)
        
class Logout(BaseView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return JsonResponse({ 'data': 'Logged out.'}, status=200)