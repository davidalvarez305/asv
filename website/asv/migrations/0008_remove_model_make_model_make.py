# Generated by Django 4.0.3 on 2023-05-01 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asv', '0007_remove_trim_model_trim_model_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='model',
            name='make',
        ),
        migrations.AddField(
            model_name='model',
            name='make',
            field=models.ManyToManyField(to='asv.make'),
        ),
    ]