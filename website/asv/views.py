import os
from django.shortcuts import render

from website.asv.models import Truck

def home(request):
    return render(request, 'asv/home.html')