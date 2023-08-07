import os
from posixpath import abspath
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from asv.models import Branch, Sale, Truck, VehicleCondition, VehicleDetails, Make, Model, Trim
from asv.utils.upload_file import handle_uploaded_file, parse_csv_file
from asv.utils.bulk_insert_data import bulk_insert_data
from asv.utils.upload_to_s3 import upload_to_s3
import datetime as dt
import paramiko

from asv.utils.truck_list import TRUCK_LIST

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
        params = request.GET.dict()

        make = params.get('truck')
        if make is None:
            return render(request, self.template_name)

        years = VehicleDetails.objects.distinct("year").order_by("year").values("year").filter(make__make=make)
        cabtypes = VehicleDetails.objects.distinct("cabtype").order_by("cabtype").values("cabtype").filter(make__make=make)
        fueltypes = VehicleDetails.objects.distinct("fueltype").order_by("fueltype").values("fueltype").filter(make__make=make)
        enginesizes = VehicleDetails.objects.distinct("enginesize").order_by("enginesize").values("enginesize").filter(make__make=make)
        odometerreadingtypedescriptions = VehicleDetails.objects.distinct("odometerreadingtypedescription").order_by("odometerreadingtypedescription").values("odometerreadingtypedescription").filter(make__make=make)
        drivelinetypes = VehicleDetails.objects.distinct("drivelinetype").order_by("drivelinetype").values("drivelinetype").filter(make__make=make)

        makes = Make.objects.order_by("make").values("id", "make").filter(make=make)
        models = Model.objects.order_by("model").values("id", "model").filter(make__make=make)
        trims = Trim.objects.order_by("trim").values("id", "trim").filter(model__make__make=make)

        yes_or_no = ["Yes", "No"]
        starts_at_checkin = ["Yes", "No", "N/A"]
        runs_and_drives = yes_or_no
        air_bags_deployed = yes_or_no
        damage_description_primarys = VehicleCondition.objects.distinct("damage_description_primary").order_by("damage_description_primary").values("damage_description_primary").filter(vehicledetails__make__make=make)
        loss_types = VehicleCondition.objects.distinct("loss_type").order_by("loss_type").values("loss_type").filter(vehicledetails__make__make=make)

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

        # X time ago
        form_time = int(params['sale__sale_date__gte'])
        params['sale__sale_date__gte'] = dt.date.today() - dt.timedelta(days=form_time * 30)

        trucks_qs = Truck.objects.select_related('vehicle_details',
                                                                  'vehicle_details__vehicle_condition',
                                                                  'vehicle_details__make',
                                                                  'vehicle_details__model',
                                                                  'vehicle_details__trim',
                                                                  'sale__branch'
                                                                  ).filter(**params).order_by('sale__sale_date')
        trucks = []
        for truck in trucks_qs:
            data = {
                "id": truck.id,
                "sale_date": truck.sale.sale_date,
                "vin": truck.vin,
                "saledocumenttype": truck.sale.saledocumenttype,
                "loss_type": truck.vehicle_details.vehicle_condition.loss_type,
                "damage_description_primary": truck.vehicle_details.vehicle_condition.damage_description_primary,
                "starts_at_checkin": truck.vehicle_details.vehicle_condition.starts_at_checkin,
                "runs_and_drives": truck.vehicle_details.vehicle_condition.runs_and_drives,
                "miles": truck.vehicle_details.vehicle_condition.miles,
                "offer": truck.offer,
                "odometerreadingtypedescription": truck.vehicle_details.odometerreadingtypedescription,
                "air_bags_deployed": truck.vehicle_details.vehicle_condition.air_bags_deployed,
                "saleprice": truck.sale.saleprice,
                "branch": truck.sale.branch.branch,
                "branch_zip_code": truck.sale.branch.branch_zip_code,
                "drivelinetype": truck.vehicle_details.drivelinetype,
                "year": truck.vehicle_details.year,
                "make": truck.vehicle_details.make.make,
                "model": truck.vehicle_details.model.model,
                "trim": truck.vehicle_details.trim.trim,
                "bodytype": truck.vehicle_details.bodytype,
                "cabtype": truck.vehicle_details.cabtype,
                "fueltype": truck.vehicle_details.fueltype,
                "enginesize": truck.vehicle_details.enginesize,
                "data_type": truck.data_type,
                "stateabbreviation": truck.sale.branch.stateabbreviation,
            }
            trucks.append(data)
        
        print('TRUCKS: ', len(trucks))
        return JsonResponse({ 'data': trucks })
    
    def delete(self, request, *args, **kwargs):
        qs = Truck.objects.select_related('vehicle_details',
                                                            'vehicle_details__vehicle_condition',
                                                            'vehicle_details__make',
                                                            'vehicle_details__model',
                                                            'vehicle_details__trim',
                                                            'sale__branch')
        trucks = []
        vehicle_details = []
        vehicle_condition = []
        branches = []
        sales = []
        lowercase_truck_list = [item.lower() for item in TRUCK_LIST]

        for truck in qs:
            if truck.vehicle_details.cabtype.lower() not in lowercase_truck_list:
                vehicle_details.append(truck.vehicle_details.id)
                vehicle_condition.append(truck.vehicle_details.vehicle_condition.id)
                branches.append(truck.sale.branch.id)
                sales.append(truck.sale.id)
                trucks.append(truck.id)

        Truck.objects.filter(id__in=trucks).delete()
        VehicleDetails.objects.filter(id__in=vehicle_details).delete()
        VehicleCondition.objects.filter(id__in=vehicle_condition).delete()
        Branch.objects.filter(id__in=branches).delete()
        Sale.objects.filter(id__in=sales).delete()

        return JsonResponse({ 'data': len(trucks) })
    
class Upload(LoginRequiredMixin, BaseView):
    login_url="/login"
    template_name = 'asv/upload.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        file = request.FILES["upload_file"]

        if not str(file).endswith(".csv"):
            return HttpResponseBadRequest("CSV Only.")
        
        updated_file_name = format(dt.date.today().replace(day=1) - dt.timedelta(days=1), '%Y_%B.csv')
        local_path = abspath('../website/uploads/' + updated_file_name)

        data = handle_uploaded_file(file=file, file_write_path=local_path)

        try:
            bulk_insert_data(data)
            return render(request, self.template_name)
        except BaseException as err:
            print("Error: ", err)
            return HttpResponseBadRequest("Bulk insert failed")
        finally:
            upload_to_s3(filename=updated_file_name, localpath=local_path)
            os.remove(local_path)
    
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

class Download(BaseView):
    def post(self, request, *args, **kwargs):
        
        FILE_NAME = format(dt.date.today().replace(day=1) - dt.timedelta(days=1), '%Y_%B.csv')
        LOCAL_PATH = abspath('../website/uploads/' + FILE_NAME)

        # Download File From FTP
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(os.environ.get('FTP_HOST'), username=os.environ.get('FTP_USERNAME'), password=os.environ.get('FTP_PASSWORD'))
        
            sftp = ssh.open_sftp()

            sftp.get(remotepath=os.environ.get('FTP_PATH'), localpath=LOCAL_PATH)

        # Parse File
        data = parse_csv_file(file_path=LOCAL_PATH)

        try:
            bulk_insert_data(data)
            return JsonResponse({ 'data': 'Success.'}, status=200)
        except BaseException as err:
            return JsonResponse({ 'data': 'Failed.'}, status=500)
        finally:
            upload_to_s3(filename=FILE_NAME, localpath=LOCAL_PATH)
            os.remove(LOCAL_PATH)