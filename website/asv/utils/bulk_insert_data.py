
import datetime
from django.db import transaction
from asv.models import Truck, VehicleCondition, VehicleDetails, Make, Model, Trim, Branch, Sale
from asv.utils.truck_list import TRUCK_LIST

def bulk_insert_data(data):
    lowercase_truck_list = [item.lower() for item in TRUCK_LIST]
    step = 1000
    for i in range(0, len(data), step):
        
        rows = data[i:i+step]
        trucks_to_create = []
        
        try:
            with transaction.atomic():
                for row in rows:
                    if row.get('CabType').lower() in lowercase_truck_list:

                        sale_date = ""

                        trim = None

                        if not '\ufeffSale_Date' in row:
                            sale_date = row.get('Sale_Date')
                        else:
                            sale_date = row.get('\ufeffSale_Date')

                        make = Make.objects.get_or_create(make=str(row.get('Make')).strip())[0]
                        model = Model.objects.get_or_create(model=str(row.get('Model')).strip())[0]
                        model.make.add(make)
                        model.save()
                    
                        if row.get('Trim') is not None:
                            trim = Trim.objects.get_or_create(trim=row.get('Trim').strip())[0]
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
                            sale_date=datetime.strptime(sale_date, '%m/%d/%Y').date(),
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
                
                    print(f"Inserting {i + step} of {len(data)}")
                Truck.objects.bulk_create(trucks_to_create)
        except BaseException as err:
            print("ERROR: ", err)
            continue
