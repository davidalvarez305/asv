from django.db import migrations, models
from datetime import datetime

def convert_to_date(apps, schema_editor):
    # Get the model of the target table
    ASV_Sale = apps.get_model('asv', 'Sale')

    # Retrieve all instances of the model
    instances = ASV_Sale.objects.all()

    # Convert the date strings to date objects and update the new date column
    for instance in instances:
        instance.sale_date_new = datetime.strptime(instance.sale_date, '%m/%d/%Y').date()
        instance.save()

class Migration(migrations.Migration):

    dependencies = [
        ('asv', '0009_sale_sale_date_new'),  # Replace with your previous migration's name
    ]

    operations = [
        migrations.RunPython(convert_to_date),
    ]