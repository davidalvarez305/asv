# Generated by Django 4.0.3 on 2023-05-01 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asv', '0004_alter_truck_vin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('branch', models.CharField(max_length=255, null=True)),
                ('branch_zip_code', models.CharField(max_length=255, null=True)),
                ('stateabbreviation', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Make',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('make', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('model', models.CharField(max_length=255)),
                ('make', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asv.make')),
            ],
        ),
        migrations.CreateModel(
            name='Trim',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('trim', models.CharField(max_length=255)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asv.model')),
            ],
        ),
        migrations.CreateModel(
            name='VehicleCondition',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('starts_at_checkin', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'N/A')], max_length=255, null=True)),
                ('runs_and_drives', models.CharField(choices=[('No', 'No'), ('Yes', 'Yes')], max_length=255, null=True)),
                ('air_bags_deployed', models.CharField(choices=[('No', 'No'), ('Yes', 'Yes')], max_length=255, null=True)),
                ('miles', models.CharField(max_length=255, null=True)),
                ('damage_description_primary', models.CharField(max_length=255, null=True)),
                ('loss_type', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='truck',
            name='air_bags_deployed',
        ),
        migrations.RemoveField(
            model_name='truck',
            name='bodytype',
        ),
        migrations.RemoveField(
            model_name='truck',
            name='branch',
        ),
        migrations.RemoveField(
            model_name='truck',
            name='branch_zip_code',
        ),
        migrations.RemoveField(
            model_name='truck',
            name='cabtype',
        ),
        migrations.RemoveField(
            model_name='truck',
            name='damage_description_primary',
        ),
        migrations.RemoveField(
            model_name='truck',
            name='drivelinetype',
        ),
        migrations.RemoveField(
            model_name='truck',
            name='enginesize',
        ),
        migrations.RemoveField(
            model_name='truck',
            name='fueltype',
        ),
        migrations.RemoveField(
            model_name='truck',
            name='loss_type',
        ),
        migrations.RemoveField(
            model_name='truck',
            name='make',
        ),
        migrations.RemoveField(
            model_name='truck',
            name='miles',
        ),
        migrations.RemoveField(
            model_name='truck',
            name='model',
        ),
        migrations.RemoveField(
            model_name='truck',
            name='odometerreadingtypedescription',
        ),
        migrations.RemoveField(
            model_name='truck',
            name='runs_and_drives',
        ),
        migrations.RemoveField(
            model_name='truck',
            name='sale_date',
        ),
        migrations.RemoveField(
            model_name='truck',
            name='saledocumenttype',
        ),
        migrations.RemoveField(
            model_name='truck',
            name='saleprice',
        ),
        migrations.RemoveField(
            model_name='truck',
            name='starts_at_checkin',
        ),
        migrations.RemoveField(
            model_name='truck',
            name='stateabbreviation',
        ),
        migrations.RemoveField(
            model_name='truck',
            name='trim',
        ),
        migrations.RemoveField(
            model_name='truck',
            name='year',
        ),
        migrations.AlterField(
            model_name='truck',
            name='data_type',
            field=models.CharField(choices=[('Insurance', 'Insurance'), ('Non-Insurance', 'Non-Insurance')], max_length=255, null=True),
        ),
        migrations.CreateModel(
            name='VehicleDetails',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('year', models.CharField(max_length=255)),
                ('bodytype', models.CharField(max_length=255, null=True)),
                ('cabtype', models.CharField(max_length=255, null=True)),
                ('fueltype', models.CharField(max_length=255, null=True)),
                ('enginesize', models.CharField(max_length=255, null=True)),
                ('odometerreadingtypedescription', models.TextField()),
                ('drivelinetype', models.CharField(max_length=255, null=True)),
                ('make', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asv.make')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asv.model')),
                ('trim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asv.trim')),
                ('vehicle_condition', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='asv.vehiclecondition')),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('saledocumenttype', models.CharField(max_length=255, null=True)),
                ('saleprice', models.CharField(max_length=255, null=True)),
                ('sale_date', models.CharField(max_length=255)),
                ('branch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='asv.branch')),
            ],
        ),
        migrations.AddField(
            model_name='truck',
            name='sale',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='asv.sale'),
        ),
        migrations.AddField(
            model_name='truck',
            name='vehicle_details',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='asv.vehicledetails'),
        ),
    ]
