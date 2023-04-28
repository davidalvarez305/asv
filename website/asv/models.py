from django.db import models

class Truck(models.Model):
    id = models.BigAutoField(primary_key=True)
    sale_date = models.CharField(max_length=255)
    vin = models.CharField(max_length=255)
    saledocumenttype = models.CharField(max_length=255, null=True)
    loss_type = models.CharField(max_length=255, null=True)
    damage_description_primary = models.CharField(max_length=255, null=True)
    starts_at_checkin = models.CharField(max_length=255, null=True)
    runs_and_drives = models.CharField(max_length=255, null=True)
    miles = models.CharField(max_length=255, null=True)
    offer = models.CharField(max_length=255, null=True)
    odometerreadingtypedescription = models.TextField()
    air_bags_deployed = models.CharField(max_length=255, null=True)
    saleprice = models.CharField(max_length=255, null=True)
    branch = models.CharField(max_length=255, null=True)
    branch_zip_code = models.CharField(max_length=255, null=True)
    drivelinetype = models.CharField(max_length=255, null=True)
    year = models.CharField(max_length=255)
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    trim = models.CharField(max_length=255, null=True)
    bodytype = models.CharField(max_length=255, null=True)
    cabtype = models.CharField(max_length=255, null=True)
    fueltype = models.CharField(max_length=255, null=True)
    enginesize = models.CharField(max_length=255, null=True)
    data_type = models.CharField(max_length=255, null=True)
    stateabbreviation = models.CharField(max_length=5)

    def __str__(self):
        return self.year + self.make + self.model + self.trim