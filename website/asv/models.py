from django.db import models

class Truck(models.Model):
    id = models.BigAutoField(primary_key=True)
    sale_date = models.DateField()
    vin = models.CharField(max_length=255, unique=True)
    saledocumenttype = models.CharField(max_length=255)
    loss_type = models.CharField(max_length=255)
    damage_description_primary = models.CharField(max_length=255)
    starts_at_checkin = models.BooleanField()
    runs_and_drives = models.BooleanField()
    miles = models.PositiveIntegerField()
    offer = models.PositiveIntegerField()
    odometerreadingtypedescription = models.TextField()
    air_bags_deployed = models.BooleanField()
    saleprice = models.PositiveIntegerField()
    branch = models.CharField(max_length=255)
    branch_zip_code = models.CharField(max_length=255)
    drivelinetype = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    trim = models.CharField(max_length=255, null=True)
    bodytype = models.CharField(max_length=255, null=True)
    cabtype = models.CharField(max_length=255)
    fueltype = models.CharField(max_length=255)
    enginesize = models.CharField(max_length=255)
    data_type = models.CharField(max_length=255)
    stateabbreviation = models.CharField(max_length=2)

    def __str__(self):
        return self.year + self.make + self.model + self.trim