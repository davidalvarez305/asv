# Generated by Django 4.0.3 on 2023-05-01 20:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asv', '0006_alter_make_make_alter_model_model_alter_trim_trim'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trim',
            name='model',
        ),
        migrations.AddField(
            model_name='trim',
            name='model',
            field=models.ManyToManyField(to='asv.model'),
        ),
        migrations.AlterField(
            model_name='vehicledetails',
            name='trim',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='asv.trim'),
        ),
    ]
