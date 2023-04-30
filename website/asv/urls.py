from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('trucks', views.Trucks.as_view(), name='trucks'),
    path('upload', views.Upload.as_view(), name='upload'),
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout')
]