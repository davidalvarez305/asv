from django.db import models

DATA_TYPE_CHOICES = [
    ("Insurance", "Insurance"),
    ("Non-Insurance", "Non-Insurance")
]

STARTS_AT_CHECK_IN_CHOICES = [
    ("Yes", "Yes"),
    ("No", "No"),
    ("N/A", "N/A")
]

YES_NO_CHOICES = [
    ("No", "No"),
    ("Yes", "Yes")
]

class VehicleCondition(models.Model):
    id = models.BigAutoField(primary_key=True)
    starts_at_checkin = models.CharField(max_length=255, null=True, choices=STARTS_AT_CHECK_IN_CHOICES)
    runs_and_drives = models.CharField(max_length=255, null=True, choices=YES_NO_CHOICES)
    air_bags_deployed = models.CharField(max_length=255, null=True, choices=YES_NO_CHOICES)
    miles = models.CharField(max_length=255, null=True)
    damage_description_primary = models.CharField(max_length=255, null=True)
    loss_type = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.id

class Make(models.Model):
    id = models.BigAutoField(primary_key=True)
    make = models.CharField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.make

class Model(models.Model):
    id = models.BigAutoField(primary_key=True)
    model = models.CharField(max_length=255, unique=True, db_index=True)
    make = models.ManyToManyField(Make)

    def __str__(self):
        return self.model

class Trim(models.Model):
    id = models.BigAutoField(primary_key=True)
    trim = models.CharField(max_length=255, unique=True, db_index=True)
    model = models.ManyToManyField(Model)

    def __str__(self):
        return self.trim

class VehicleDetails(models.Model):
    id = models.BigAutoField(primary_key=True)
    year = models.CharField(max_length=255)
    make = models.ForeignKey(Make, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    trim = models.ForeignKey(Trim, on_delete=models.CASCADE, null=True)
    bodytype = models.CharField(max_length=255, null=True)
    cabtype = models.CharField(max_length=255, null=True)
    fueltype = models.CharField(max_length=255, null=True)
    enginesize = models.CharField(max_length=255, null=True)
    odometerreadingtypedescription = models.TextField()
    drivelinetype = models.CharField(max_length=255, null=True)
    vehicle_condition = models.ForeignKey(VehicleCondition, on_delete=models.SET_NULL, null=True, db_index=True)

    def __str__(self):
        return self.year + self.make + self.model + self.trim

class Branch(models.Model):
    id = models.BigAutoField(primary_key=True)
    branch = models.CharField(max_length=255, null=True)
    branch_zip_code = models.CharField(max_length=255, null=True)
    stateabbreviation = models.CharField(max_length=2)

    def __str__(self):
        return self.branch

class Sale(models.Model):
    id = models.BigAutoField(primary_key=True)
    saledocumenttype = models.CharField(max_length=255, null=True)
    saleprice = models.CharField(max_length=255, null=True)
    sale_date = models.CharField(max_length=255)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, db_index=True)

    def __str__(self):
        return self.id

class Truck(models.Model):
    id = models.BigAutoField(primary_key=True)
    vin = models.CharField(max_length=255)
    data_type = models.CharField(max_length=255, null=True, choices=DATA_TYPE_CHOICES)
    offer = models.CharField(max_length=255, null=True)
    sale = models.ForeignKey(Sale, on_delete=models.SET_NULL, null=True, db_index=True)
    vehicle_details = models.ForeignKey(VehicleDetails, on_delete=models.SET_NULL, null=True, db_index=True)

    def __str__(self):
        return self.vin