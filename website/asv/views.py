import os
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction

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

        years = VehicleDetails.objects.distinct("year").values("year")
        cabtypes = VehicleDetails.objects.distinct("cabtype").values("cabtype")
        fueltypes = VehicleDetails.objects.distinct("fueltype").values("fueltype")
        enginesizes = VehicleDetails.objects.distinct("enginesize").values("enginesize")
        odometerreadingtypedescriptions = VehicleDetails.objects.distinct("odometerreadingtypedescription").values("odometerreadingtypedescription")
        drivelinetypes = VehicleDetails.objects.distinct("drivelinetype").values("drivelinetype")

        makes = Make.objects.values("id", "make")
        models = Model.objects.values("id", "model")
        trims = Trim.objects.values("id", "trim")

        yes_or_no = ["Yes", "No"]
        starts_at_checkin = ["Yes", "No", "N/A"]
        runs_and_drives = yes_or_no
        air_bags_deployed = yes_or_no
        damage_description_primarys = VehicleCondition.objects.distinct("damage_description_primary").values("damage_description_primary")
        loss_types = VehicleCondition.objects.distinct("loss_type").values("loss_type")

        context = {}
        context["makes"] = makes
        context["models"] = models
        context["trims"] = trims
        context["years"] = years
        context["cabtypes"] = cabtypes
        context["fueltypes"] = fueltypes
        context["enginesizes"] = enginesizes
        context["odometerreadingtypedescriptions"] = odometerreadingtypedescriptions
        context["drivelinetypes"] = drivelinetypes
        context["starts_at_checkin"] = starts_at_checkin
        context["runs_and_drives"] = runs_and_drives
        context["air_bags_deployed"] = air_bags_deployed
        context["damage_description_primarys"] = damage_description_primarys
        context["loss_types"] = loss_types

        return render(request, self.template_name, context=context)
    
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

        if not file.endswith(".csv"):
            return HttpResponseBadRequest("CSV Only.")

        with transaction.atomic():
            trucks_to_create = []
            data = handle_uploaded_file(file)

            for row in data:
                sale_date = ""
                trim = None

                if not '\ufeffSale_Date' in row:
                    sale_date = row.get('Sale_Date')
                else:
                    sale_date = row.get('\ufeffSale_Date')

                make = Make.objects.get_or_create(make=row.get('Make'))[0]
                model = Model.objects.get_or_create(model=row.get('Model'))[0]
                model.make.add(make)
                model.save()
            
                if row.get('Trim') is not None:
                    trim = Trim.objects.get_or_create(trim=row.get('Trim'))[0]
                    trim.model.add(model)
                    trim.save()
                
                vehicle_details = VehicleDetails.objects.create(
                    year=row.get('Year'),
                    make=make,
                    model = model,
                    trim = trim,
                    bodytype=row.get('BodyType'),
                    cabtype=row.get('CabType'),
                    fueltype=row.get('FuelType'),
                    enginesize=row.get('EngineSize'),
                    odometerreadingtypedescription=row.get('OdometerReadingTypeDescription'),
                    drivelinetype=row.get('DriveLineType'),
                    vehicle_condition = VehicleCondition.objects.create(
                        starts_at_checkin=row.get('Starts_At_CheckIn'),
                        runs_and_drives=row.get('Runs_And_Drives'),
                        air_bags_deployed=row.get('Air_Bags_Deployed'),
                        miles=row.get('Miles'),
                        loss_type=row.get('Loss_Type'),
                        damage_description_primary=row.get('Damage_Description_Primary'),
                    ),
                )

                branch = Branch.objects.create(
                    branch=row.get('Branch'),
                    branch_zip_code=row.get('Branch_Zip_Code'),
                    stateabbreviation=row.get('StateAbbreviation')
                )

                sale = Sale.objects.create(
                    sale_date=sale_date,
                    saleprice=row.get('SalePrice'),
                    saledocumenttype=row.get('SaleDocumentType'),
                    branch = branch
                )

                truck = Truck(
                    vin=row.get('VIN'),
                    data_type=row.get('Data_Type'),
                    offer=row.get('Offer'),
                    vehicle_details = vehicle_details,
                    sale = sale,
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